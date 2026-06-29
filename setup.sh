#!/usr/bin/env bash
# LoopSpec Bootstrap — Unix/macOS
# https://github.com/loopspec/loopspec
set -euo pipefail

# ── Colors ───────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'

# ── Resolve paths ────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_DIR="$SCRIPT_DIR/templates"
TARGET_DIR="${1:-.}"
LOOPSPEC_DIR="$TARGET_DIR/.loopspec"
ITERATIONS_DIR="$LOOPSPEC_DIR/iterations"
AGENTS_FILE="$TARGET_DIR/AGENTS.md"

# ── Preflight checks ────────────────────────────────────────────────
if [ ! -d "$TEMPLATE_DIR" ]; then
  echo -e "${RED}✗ Error:${NC} templates/ directory not found at ${TEMPLATE_DIR}"
  echo "  Make sure you run this script from the LoopSpec installation directory."
  exit 1
fi

if [ -d "$LOOPSPEC_DIR" ]; then
  echo -e "${YELLOW}⚠ Warning:${NC} ${BOLD}.loopspec/${NC} already exists in ${TARGET_DIR}"
  echo "  To avoid overwriting your existing configuration, this script will exit."
  echo "  Remove .loopspec/ manually if you want to re-initialize."
  exit 1
fi

# ── Create directory structure ───────────────────────────────────────
echo -e "${BLUE}▸${NC} Creating .loopspec/ directory structure..."
mkdir -p "$ITERATIONS_DIR"

# ── Copy template files ─────────────────────────────────────────────
echo -e "${BLUE}▸${NC} Copying template files..."
COPIED=0
for tmpl in "$TEMPLATE_DIR"/*.md; do
  [ -f "$tmpl" ] || continue
  cp "$tmpl" "$LOOPSPEC_DIR/"
  COPIED=$((COPIED + 1))
done

if [ "$COPIED" -eq 0 ]; then
  echo -e "${RED}✗ Error:${NC} No .md template files found in ${TEMPLATE_DIR}"
  rm -rf "$LOOPSPEC_DIR"
  exit 1
fi

echo -e "${GREEN}  ✓${NC} Copied ${COPIED} template files"

# ── Generate AGENTS.md at project root ───────────────────────────────
echo -e "${BLUE}▸${NC} Generating AGENTS.md at project root..."
cat > "$AGENTS_FILE" <<'AGENTS_EOF'
# AGENTS.md

> This project uses [LoopSpec](https://github.com/loopspec/loopspec) — a self-correcting AI development protocol.

## Instructions for AI Agents

Before making any changes to this project, read and follow the LoopSpec protocol:

1. **Read** `.loopspec/PROTOCOL.md` for the complete operating manual
2. **Read** `.loopspec/GOAL.md` for the current objective and success criteria
3. **Read** `.loopspec/STATUS.md` for the current execution state
4. **Read** `.loopspec/LEARNINGS.md` for past mistakes to avoid

Follow the LoopSpec phases: ANALYZE → PLAN → TEST → IMPLEMENT → VERIFY → EVALUATE

Do not skip phases. Do not proceed without human approval on PLAN.md.
AGENTS_EOF
echo -e "${GREEN}  ✓${NC} AGENTS.md created"

# ── Success banner ───────────────────────────────────────────────────
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  ✓ LoopSpec initialized successfully!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BOLD}Getting started:${NC}"
echo ""
echo -e "  ${CYAN}1.${NC} Define your goal and success criteria:"
echo -e "     ${YELLOW}\$EDITOR .loopspec/GOAL.md${NC}"
echo ""
echo -e "  ${CYAN}2.${NC} Open the project with your AI coding tool"
echo ""
echo -e "  ${CYAN}3.${NC} Tell the AI to read the protocol:"
echo -e "     ${YELLOW}\"Read .loopspec/PROTOCOL.md and begin.\"${NC}"
echo ""
echo -e "${BOLD}Directory layout:${NC}"
echo ""
echo -e "  ${BLUE}.loopspec/${NC}"
for f in "$LOOPSPEC_DIR"/*.md; do
  [ -f "$f" ] || continue
  echo -e "  ├── $(basename "$f")"
done
echo -e "  └── ${BLUE}iterations/${NC}"
echo ""
echo -e "  AGENTS.md  ${GREEN}(auto-generated — AI agent entry point)${NC}"
echo ""
echo -e "${BOLD}Learn more:${NC} ${CYAN}https://github.com/loopspec/loopspec${NC}"
echo ""
