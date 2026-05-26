#!/usr/bin/env bash
# Copy-only sync: lab education tree -> this Public staging repo.
# Never deletes or modifies files under the lab source path.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STAGE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
LAB_ROOT="${LAB_ROOT:-/mnt/ai_lab_os/AI_LAB/qi/education/ai-engineering-fliinxster}"

if [[ ! -d "$LAB_ROOT" ]]; then
  echo "Lab root not found: $LAB_ROOT" >&2
  echo "Set LAB_ROOT to your ai-engineering-fliinxster path." >&2
  exit 1
fi

echo "Sync (copy-only): $LAB_ROOT -> $STAGE_ROOT"

copy_file() {
  local src="$1" dest="$2"
  mkdir -p "$(dirname "$dest")"
  cp "$src" "$dest"
}

copy_file "$LAB_ROOT/INDEX.md" "$STAGE_ROOT/INDEX.md"
copy_file "$LAB_ROOT/python_cheatsheet.md" "$STAGE_ROOT/python_cheatsheet.md"
copy_file "$LAB_ROOT/projects/README.md" "$STAGE_ROOT/projects/README.md"

for readme in "$LAB_ROOT"/projects/*/README.md; do
  [[ -f "$readme" ]] || continue
  mod="$(basename "$(dirname "$readme")")"
  copy_file "$readme" "$STAGE_ROOT/projects/$mod/README.md"
done

# Copy learner code from lab modules if present (never PDFs or secrets)
for mod_dir in "$LAB_ROOT"/projects/*/; do
  mod="$(basename "$mod_dir")"
  dest_mod="$STAGE_ROOT/projects/$mod"
  mkdir -p "$dest_mod"
  while IFS= read -r -d '' f; do
    base="$(basename "$f")"
    case "$base" in
      .env|.env.*|*.pdf) continue ;;
    esac
    cp "$f" "$dest_mod/$base"
  done < <(find "$mod_dir" -maxdepth 1 -type f \( -name '*.py' -o -name '*.txt' \) -print0 2>/dev/null)
done

echo "Done. Review with: cd $STAGE_ROOT && git status"
echo "Excluded: *.pdf, .env, .venv/, output/, screenshots/"
