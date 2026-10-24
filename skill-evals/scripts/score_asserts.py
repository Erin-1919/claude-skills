"""Fraction of regex asserts passed per trial, averaged per case, from saved outputs."""
import json, re, sys, glob, os, statistics
casefile, *dirs = sys.argv[1:]
cases = {c["id"]: c for c in json.load(open(casefile, encoding="utf-8"))["cases"]}
for d in dirs:
    tot = []
    print("==", os.path.basename(d))
    for cid, c in cases.items():
        fr = []
        for f in sorted(glob.glob(os.path.join(d, f"skill-{cid}-t*.txt"))):
            out = open(f, encoding="utf-8").read()
            m = re.search(c.get("extract", "(.*)"), out, re.S)
            out = m.group(1) if m else out
            asserts = [(p, True) for p in c.get("expect", [])] + [(p, False) for p in c.get("forbid", [])]
            ok = sum((re.search(p, out, re.I | re.S) is not None) == want for p, want in asserts)
            fr.append(ok / len(asserts))
        if fr:
            print(f"  {cid:24s} {statistics.mean(fr):.2f}")
            tot.append(statistics.mean(fr))
    print(f"  {'MEAN':24s} {statistics.mean(tot):.2f}")
