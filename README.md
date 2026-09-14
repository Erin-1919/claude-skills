# Claude Code skills

Personal Claude Code skills, synced across devices.

## Setup on a new device

```bash
# ~/.claude/skills must not already exist (or must be empty)
git clone git@github.com:Erin-1919/claude-skills.git ~/.claude/skills
```

Afterwards, `git pull` in `~/.claude/skills` to pick up changes from other devices.

## Scope

This repo covers **personal skills only**. Plugin-provided skills (superpowers,
understand-anything, code-review, …) live in `~/.claude/plugins/` and are managed by
the plugin marketplace — install the same plugins on each device rather than syncing
them here.

## Vendored skills

Two skills were cloned from upstream and are vendored here (their `.git` dirs were
removed so they track as plain files):

| Skill | Upstream | Vendored at |
|---|---|---|
| `academic-humanizer` | https://github.com/AIScientists-Dev/academic-humanizer | `94b88b2` |
| `scipilot-figure-skill` | https://github.com/Haojae/scipilot-figure-skill | `43098dd` |

To update one, pull the upstream repo elsewhere and copy the files over.
