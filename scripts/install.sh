#!/usr/bin/env bash
# === harness-traj-weaver install ===
# Run once after cloning the skill:
#   git clone ... ~/.claude/skills/harness-traj-weaver
#   ~/.claude/skills/harness-traj-weaver/install.sh [--target /path/to/repo]
#
# What it does:
#   1. Register skill in ~/.claude/settings.json
#   2. Install pre-commit + pre-push hooks into target repo's .git/hooks/

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_NAME="harness-traj-weaver"
TARGET="${1:-$(pwd)}"

echo "=== harness-traj-weaver install ==="
echo "  Skill:  $SKILL_DIR"
echo "  Target: $TARGET"
echo ""

# ── Step 1: Register skill ──
SETTINGS="$HOME/.claude/settings.json"
if [ ! -f "$SETTINGS" ]; then
    echo '{"skills":{}}' > "$SETTINGS"
fi

# Check if already registered
if python -c "
import json, sys
with open('$SETTINGS') as f:
    cfg = json.load(f)
if 'skills' in cfg and '$SKILL_NAME' in cfg.get('skills',{}):
    sys.exit(0)
else:
    sys.exit(1)
" 2>/dev/null; then
    echo "  (skill already registered)"
else
    python -c "
import json
with open('$SETTINGS') as f:
    cfg = json.load(f)
cfg.setdefault('skills',{})['$SKILL_NAME'] = '$SKILL_DIR'
with open('$SETTINGS','w') as f:
    json.dump(cfg, f, indent=2)
" 2>/dev/null && echo "  Registered in ~/.claude/settings.json" || echo "  (could not register — add manually)"
fi

# ── Step 2: Install hooks into target repo ──
if [ ! -d "$TARGET/.git" ]; then
    echo "  Target is not a git repo: $TARGET"
    echo "  Run: install.sh /path/to/your/repo"
    exit 1
fi

cp "$SKILL_DIR/hooks/pre-commit" "$TARGET/.git/hooks/pre-commit"
cp "$SKILL_DIR/hooks/pre-push" "$TARGET/.git/hooks/pre-push"
chmod +x "$TARGET/.git/hooks/pre-commit" "$TARGET/.git/hooks/pre-push"

echo "  Hooks installed:"
echo "    $TARGET/.git/hooks/pre-commit"
echo "    $TARGET/.git/hooks/pre-push"
echo ""
echo "Done. The skill will auto-load on next session start."
echo "Hooks will fire on git commit / git push in $TARGET."
