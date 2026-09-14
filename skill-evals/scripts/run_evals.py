#!/usr/bin/env python3
"""Minimal skill-eval harness. Stdlib only.

Runs each case in a fresh temp workspace, N trials each, and scores trigger
behaviour plus regex / workspace-check / judge asserts. The ablation arm re-runs
the same cases with all skills disabled, to show whether the skill does anything.

    # trigger-only: agent cannot write files or run shell commands (default)
    python run_evals.py evals.json --skill ~/.claude/skills/my-skill --ablation

    # outcome mode: agent may act. Only for skills whose result must be inspected.
    python run_evals.py evals.json --skill ~/.claude/skills/my-skill --mode act

Isolation note: the workspace is always a fresh temp dir, which is the real
cheating vector (ambient files, git history, sibling code). The config dir is
inherited by default because a fresh one has no credentials; pass --config-dir
only if you have set that dir up with working auth.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

CLAUDE = shutil.which("claude") or "claude"
BASH = shutil.which("bash")
SAVE_DIR = None   # set by --save-outputs; keeps raw agent output for diagnosis

# Trigger-only mode: the agent may think and call the Skill tool, but cannot
# touch the filesystem or shell. Keeps evals of destructive skills safe.
READONLY_DENY = ["Bash", "Write", "Edit", "NotebookEdit"]


# --------------------------------------------------------------------------- run

def _agent(prompt, cwd, config_dir, model, timeout, skills=True, readonly=True):
    """Run the coding agent once. Returns (final_text, tool_use_events)."""
    cmd = [CLAUDE, "-p", prompt, "--output-format", "stream-json", "--verbose"]
    if readonly:
        cmd += ["--disallowedTools"] + READONLY_DENY
    if not skills:
        cmd += ["--disable-slash-commands"]      # ablation arm
    if model:
        cmd += ["--model", model]

    env = dict(os.environ)
    if config_dir:
        env["CLAUDE_CONFIG_DIR"] = str(config_dir)
    env["PYTHONUTF8"] = "1"

    try:
        proc = subprocess.run(cmd, cwd=str(cwd), env=env, capture_output=True,
                              text=True, encoding="utf-8", errors="replace",
                              timeout=timeout)
    except subprocess.TimeoutExpired:
        return "<TIMEOUT>", []
    except FileNotFoundError:
        sys.exit("error: 'claude' not on PATH. Install Claude Code first.")

    final, tools = "", []
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") == "result":
            final = ev.get("result") or final
        msg = ev.get("message") or {}
        content = msg.get("content")
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    tools.append(block)
    if not final:
        final = proc.stdout[-4000:]
    return final, tools


def _loaded_skill(tools, skill_name):
    """Did the agent actually pull the skill into context?"""
    needle = skill_name.lower()
    for t in tools:
        raw = json.dumps(t.get("input", {})).lower()
        if t.get("name") == "Skill" and needle in raw:
            return True
        # progressive disclosure: reading SKILL.md or a reference file counts
        if t.get("name") in ("Read", "Grep", "Glob") and needle in raw and "skill" in raw:
            return True
    return False


def _invoked_skills(tools):
    """Every skill the agent invoked, for diagnosing negative-case failures."""
    names = []
    for t in tools:
        if t.get("name") == "Skill":
            s = (t.get("input") or {}).get("skill")
            if s:
                names.append(s)
    return names


def _sh(cmd, cwd):
    """Run an author-supplied setup/check command in the workspace."""
    argv = [BASH, "-lc", cmd] if BASH else cmd
    return subprocess.run(argv, cwd=str(cwd), shell=(BASH is None),
                          capture_output=True, text=True, errors="replace")


# ----------------------------------------------------------------------- scoring

def _judge(rubric, output, config_dir, model, timeout):
    prompt = (rubric + "\n\n--- OUTPUT UNDER TEST ---\n" + output[:20000] +
              "\n--- END ---\nFirst line must be exactly PASS or FAIL.")
    with tempfile.TemporaryDirectory() as d:
        text, _ = _agent(prompt, Path(d), config_dir, model, timeout, readonly=True)
    lines = text.strip().splitlines()
    first = lines[0].upper() if lines else "FAIL"
    return first.startswith("PASS"), text.strip()[:400]


def _extract(case, output):
    """Narrow scoring to the deliverable.

    Agents wrap their output in commentary ("Bracketed slots are where your
    values go; I did not invent numbers"). Asserting against the wrapper
    scores the chat, not the artefact, and produces false failures.
    """
    pat = case.get("extract")
    if not pat:
        return output
    m = re.search(pat, output, re.S)
    if not m:
        return output          # no fence emitted; score the whole thing
    return m.group(1) if m.groups() else m.group(0)


def _score(case, output, loaded, ws, cfg, model, timeout):
    reasons = []
    output = _extract(case, output)
    for pat in case.get("expect", []):
        if not re.search(pat, output, re.I | re.S):
            reasons.append("missing /" + pat + "/")
    for pat in case.get("forbid", []):
        if re.search(pat, output, re.I | re.S):
            reasons.append("forbidden /" + pat + "/")

    # Trigger asserts. Note the asymmetry: a positive case does NOT require the
    # skill to load (outcomes, not paths) unless it sets require_trigger.
    if case.get("should_trigger") is False and loaded:
        reasons.append("over-triggered: skill loaded on a negative case")
    if case.get("require_trigger") and not loaded:
        reasons.append("under-triggered: skill never loaded")

    for cmd in case.get("check", []):
        r = _sh(cmd, ws)
        if r.returncode != 0:
            reasons.append("check failed: " + cmd)
    if case.get("judge"):
        ok, why = _judge(case["judge"], output, cfg, model, timeout)
        if not ok:
            reasons.append("judge FAIL: " + why)
    return {"pass": not reasons, "reasons": reasons, "loaded": loaded}


# ------------------------------------------------------------------ orchestration

def _make_workspace(case):
    ws = Path(tempfile.mkdtemp(prefix="skilleval-ws-"))
    for name, content in (case.get("files") or {}).items():
        p = ws / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    if case.get("setup"):
        _sh(case["setup"], ws)
    return ws


def run_trial(case, skill_name, skills_on, cfg, model, timeout, readonly,
              trial=0):
    ws = _make_workspace(case)
    try:
        out, tools = _agent(case["prompt"], ws, cfg, model, timeout,
                            skills=skills_on, readonly=readonly)
        res = _score(case, out, _loaded_skill(tools, skill_name), ws, cfg,
                     model, timeout)
        res["invoked"] = _invoked_skills(tools)
        if SAVE_DIR:
            tag = "%s-t%d%s" % (case["id"], trial,
                                 "" if res["pass"] else "-FAIL")
            (SAVE_DIR / (tag + ".txt")).write_text(out, encoding="utf-8")
        return res
    finally:
        shutil.rmtree(ws, ignore_errors=True)


def run_arm(cases, skill_name, skills_on, trials, cfg, model, timeout, jobs,
            readonly, label):
    print("\n=== arm: %s (%d cases x %d trials) ===" % (label, len(cases), trials),
          flush=True)
    work = [(c, t) for c in cases for t in range(trials)]

    def _one(ct):
        return ct[0]["id"], run_trial(ct[0], skill_name, skills_on, cfg, model,
                                      timeout, readonly, ct[1])

    with ThreadPoolExecutor(max_workers=jobs) as pool:
        results = list(pool.map(_one, work))

    by_case = {}
    for cid, res in results:
        by_case.setdefault(cid, []).append(res)

    rows = []
    for case in cases:
        rs = by_case.get(case["id"], [])
        rate = sum(r["pass"] for r in rs) / len(rs) if rs else 0.0
        trig = sum(r["loaded"] for r in rs) / len(rs) if rs else 0.0
        failures = sorted({x for r in rs for x in r["reasons"]})
        invoked = sorted({s for r in rs for s in r.get("invoked", [])})
        rows.append({"id": case["id"], "tags": case.get("tags", []),
                     "should_trigger": case.get("should_trigger"),
                     "pass_rate": rate, "trigger_rate": trig,
                     "failures": failures, "invoked": invoked,
                     "trials_detail": [{"pass": r["pass"], "loaded": r["loaded"],
                                        "invoked": r.get("invoked", [])} for r in rs]})
        flag = "OK  " if rate == 1 else ("FAIL" if rate == 0 else "FLAK")
        print("  [%s] %-30s pass %5.0f%%  trigger %5.0f%%"
              % (flag, case["id"], rate * 100, trig * 100), flush=True)
        for f in failures[:3]:
            print("         - " + f[:150], flush=True)
        if invoked:
            print("         invoked: " + ", ".join(invoked), flush=True)
    return rows


def main():
    ap = argparse.ArgumentParser(description="Run skill evals.")
    ap.add_argument("casefile", type=Path)
    ap.add_argument("--skill", type=Path, required=True,
                    help="path to the skill directory")
    ap.add_argument("--trials", type=int, default=3,
                    help="trials per case (3-6; agents are nondeterministic)")
    ap.add_argument("--ablation", action="store_true",
                    help="also run a baseline arm with all skills disabled")
    ap.add_argument("--mode", choices=["trigger", "act"], default="trigger",
                    help="trigger: agent cannot write or run shell (default, safe). "
                         "act: agent may act, needed for workspace 'check' asserts")
    ap.add_argument("--config-dir", type=Path, default=None,
                    help="isolated config dir; must already contain working auth")
    ap.add_argument("--model", default=None)
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--out", type=Path, default=Path("eval-report.json"))
    ap.add_argument("--save-outputs", type=Path, default=None,
                    help="directory to write each trial's raw output into, "
                         "for diagnosing failures")
    args = ap.parse_args()

    global SAVE_DIR
    if args.save_outputs:
        SAVE_DIR = args.save_outputs
        SAVE_DIR.mkdir(parents=True, exist_ok=True)

    spec = json.loads(args.casefile.read_text(encoding="utf-8"))
    cases = [c for c in spec["cases"] if not c.get("id", "").startswith("_")]
    skill_src = args.skill.expanduser().resolve()
    skill_name = spec.get("skill") or skill_src.name
    if not skill_src.is_dir():
        sys.exit("error: no skill directory at " + str(skill_src))

    readonly = args.mode == "trigger"
    if readonly and any(c.get("check") for c in cases):
        print("NOTE: 'check' asserts are skipped-by-design in trigger mode "
              "(the agent cannot act). Use --mode act to exercise them.", flush=True)
        for c in cases:
            c.pop("check", None)

    pos = sum(1 for c in cases if c.get("should_trigger"))
    neg = len(cases) - pos
    if neg == 0:
        print("WARNING: no negative cases. You cannot detect over-triggering.", flush=True)
    print("skill: %s  mode: %s  cases: %d (%d positive / %d negative)"
          % (skill_name, args.mode, len(cases), pos, neg))

    report = {"skill": skill_name, "mode": args.mode, "trials": args.trials, "arms": {}}
    report["arms"]["with_skill"] = run_arm(
        cases, skill_name, True, args.trials, args.config_dir, args.model,
        args.timeout, args.jobs, readonly, "with skills")
    if args.ablation:
        report["arms"]["without_skill"] = run_arm(
            cases, skill_name, False, args.trials, args.config_dir, args.model,
            args.timeout, args.jobs, readonly, "BASELINE (skills disabled)")

    print("\n=== summary ===")
    means = {}
    for arm, rows in report["arms"].items():
        means[arm] = statistics.mean([r["pass_rate"] for r in rows]) if rows else 0.0
        print("  %-16s %.1f%%" % (arm, means[arm] * 100))
    pos_rows = [r for r in report["arms"]["with_skill"] if r["should_trigger"]]
    neg_rows = [r for r in report["arms"]["with_skill"] if not r["should_trigger"]]
    if pos_rows:
        print("  %-16s %.1f%% (positives)"
              % ("trigger rate", statistics.mean([r["trigger_rate"] for r in pos_rows]) * 100))
    if neg_rows:
        print("  %-16s %.1f%% (negatives; lower is better)"
              % ("false trigger", statistics.mean([r["trigger_rate"] for r in neg_rows]) * 100))
    if "without_skill" in means:
        delta = means["with_skill"] - means["without_skill"]
        print("  %-16s %+.1f%%" % ("delta", delta * 100))
        if delta <= 0.0:
            print("  -> Not earning its tokens. Consider retiring the skill "
                  "(keep the eval, to catch regression).")
    report["summary"] = means
    args.out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("\nwrote " + str(args.out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
