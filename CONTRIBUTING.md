# Contributing

## Principles

- **Additive:** extend modules; do not remove lesson structure without discussion.  
- **No secrets:** never commit `.env`, API keys, or lab-specific paths (`mnt/ai_lab_os`, `05_llc`, etc.).  
- **Per-module venv:** one `.venv` per `projects/<module>/` — see [projects/README.md](projects/README.md).  
- **Small PRs:** one module or one track per pull request when possible.

## Adding or updating a module

1. Update `projects/<module>/README.md` (goal, layout, run command, **Next** link).  
2. Add or update `requirements.txt` and `.gitignore`.  
3. Add reference `.py` when behavior is stable enough to run.  
4. Map deployment notes to [python_cheatsheet.md](python_cheatsheet.md) (M01–M15) where relevant.

## Pre-push check

From repository root:

```bash
rg -i "mnt/ai_lab_os|05_llc|obversary_personal|sk-[a-zA-Z0-9]{20,}" . || true
```

Fix any matches before pushing.

## Lab → GitHub sync

If you maintain a private lab copy:

```bash
./scripts/sync-to-github.sh
cd /path/to/this/repo && git add -A && git status
```

The sync script copies from `qi/education/ai-engineering-fliinxster/` **into** this tree only; it never deletes lab files.

## Cursor (standalone clone)

Open this repo as the workspace root. Optional agents live in `.cursor/agents.json`. Set `terminal.integrated.cwd` to the clone root in your editor settings.
