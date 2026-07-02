#!/usr/bin/env bash
# LoopSpec v2 Bootstrap - Unix/macOS
# https://github.com/ChahatUpadhyay/LoopSpec
set -euo pipefail

# -- Colors (ASCII-safe fallback if terminal doesn't support) ---------
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'

# -- Parse arguments ---------------------------------------------------
REPAIR_MODE=false
for arg in "$@"; do
  case "$arg" in
    --repair|--upgrade) REPAIR_MODE=true ;;
  esac
done

# -- Resolve paths -----------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_DIR="$SCRIPT_DIR/templates"
# First non-flag argument is target dir, default to current directory
TARGET_DIR="."
for arg in "$@"; do
  case "$arg" in
    --*) ;; # skip flags
    *) TARGET_DIR="$arg"; break ;;
  esac
done

# Validate target directory exists
if [ ! -d "$TARGET_DIR" ]; then
  echo -e "${RED}[ERROR]${NC} Target directory does not exist: ${TARGET_DIR}"
  exit 1
fi

LOOPSPEC_DIR="$TARGET_DIR/.loopspec"
ITERATIONS_DIR="$LOOPSPEC_DIR/iterations"
AGENTS_FILE="$TARGET_DIR/AGENTS.md"

# -- Preflight checks --------------------------------------------------
if [ ! -d "$TEMPLATE_DIR" ]; then
  echo -e "${RED}[ERROR]${NC} templates/ directory not found at ${TEMPLATE_DIR}"
  echo "  Make sure you run this script from the LoopSpec installation directory."
  exit 1
fi

if [ -d "$LOOPSPEC_DIR" ] && [ "$REPAIR_MODE" = false ]; then
  echo -e "${YELLOW}[WARNING]${NC} .loopspec/ already exists in ${TARGET_DIR}"
  echo "  Use --repair to update template files without overwriting your data."
  echo "  Use --upgrade to upgrade protocol version (preserves GOAL, LEARNINGS, etc)."
  exit 1
fi

# -- Create directory structure ----------------------------------------
echo -e "${BLUE}[*]${NC} Creating .loopspec/ directory structure..."
mkdir -p "$ITERATIONS_DIR"

# -- Copy template files -----------------------------------------------
echo -e "${BLUE}[*]${NC} Copying template files..."
COPIED=0
SKIPPED=0
for tmpl in "$TEMPLATE_DIR"/*.md "$TEMPLATE_DIR"/*.json; do
  [ -f "$tmpl" ] || continue
  DEST="$LOOPSPEC_DIR/$(basename "$tmpl")"
  if [ -f "$DEST" ] && [ "$REPAIR_MODE" = true ]; then
    BASENAME="$(basename "$tmpl")"
    # In repair mode: only overwrite PROTOCOL.md (the operating manual)
    # Preserve user data files (GOAL, LEARNINGS, QUESTIONS, etc)
    if [ "$BASENAME" = "PROTOCOL.md" ] || [ "$BASENAME" = "STATUS.json" ]; then
      cp "$tmpl" "$DEST"
      COPIED=$((COPIED + 1))
    else
      SKIPPED=$((SKIPPED + 1))
    fi
  else
    cp "$tmpl" "$DEST"
    COPIED=$((COPIED + 1))
  fi
done

if [ "$COPIED" -eq 0 ] && [ "$SKIPPED" -eq 0 ]; then
  echo -e "${RED}[ERROR]${NC} No template files found in ${TEMPLATE_DIR}"
  # Rollback: only remove if we just created it
  if [ "$REPAIR_MODE" = false ]; then
    rm -rf "$LOOPSPEC_DIR"
  fi
  exit 1
fi

echo -e "${GREEN}  [OK]${NC} Copied ${COPIED} files, skipped ${SKIPPED} (preserved)"

# -- Handle AGENTS.md (non-destructive) --------------------------------
AGENTS_CONTENT='# AGENTS.md

> This project uses [LoopSpec v2](https://github.com/ChahatUpadhyay/LoopSpec) - a self-correcting, evidence-driven AI development protocol.

## Instructions for AI Agents

Before making any changes to this project, read and follow the LoopSpec protocol:

1. **Read** `.loopspec/PROTOCOL.md` for the complete operating manual
2. **Read** `.loopspec/GOAL.md` for the current objective and success criteria
3. **Read** `.loopspec/STATUS.md` or `.loopspec/STATUS.json` for execution state
4. **Read** `.loopspec/LEARNINGS.md` for past mistakes to avoid

Follow the LoopSpec phases: ANALYZE > PLAN > TEST > IMPLEMENT > VERIFY > ADVERSARIAL > EVALUATE

Do not skip phases. Do not proceed without human approval on PLAN.md.
Do not weaken tests or thresholds to pass criteria.'

if [ -f "$AGENTS_FILE" ]; then
  echo -e "${YELLOW}[*]${NC} AGENTS.md already exists - appending LoopSpec instructions..."
  # Check if LoopSpec section already exists
  if grep -q "LoopSpec" "$AGENTS_FILE" 2>/dev/null; then
    echo -e "${GREEN}  [OK]${NC} AGENTS.md already contains LoopSpec instructions (skipped)"
  else
    echo "" >> "$AGENTS_FILE"
    echo "---" >> "$AGENTS_FILE"
    echo "" >> "$AGENTS_FILE"
    echo "$AGENTS_CONTENT" >> "$AGENTS_FILE"
    echo -e "${GREEN}  [OK]${NC} LoopSpec instructions appended to existing AGENTS.md"
  fi
else
  echo -e "${BLUE}[*]${NC} Creating AGENTS.md at project root..."
  echo "$AGENTS_CONTENT" > "$AGENTS_FILE"
  echo -e "${GREEN}  [OK]${NC} AGENTS.md created"
fi

# -- Success banner ----------------------------------------------------
echo ""
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}  LoopSpec v2 initialized successfully!${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""
echo -e "${BOLD}Getting started:${NC}"
echo ""
echo -e "  ${CYAN}1.${NC} Define your goal and success criteria:"
echo -e "     ${YELLOW}\$EDITOR .loopspec/GOAL.md${NC}"
echo ""
echo -e "  ${CYAN}2.${NC} Open the project with your AI coding tool"
echo ""
echo -e "  ${CYAN}3.${NC} Tell the AI:"
echo -e "     ${YELLOW}\"Read .loopspec/PROTOCOL.md and begin.\"${NC}"
echo ""
echo -e "${BOLD}Directory layout:${NC}"
echo ""
echo -e "  ${BLUE}.loopspec/${NC}"
for f in "$LOOPSPEC_DIR"/*.md "$LOOPSPEC_DIR"/*.json; do
  [ -f "$f" ] || continue
  echo -e "  |-- $(basename "$f")"
done
echo -e "  |-- ${BLUE}iterations/${NC}"
echo ""
echo -e "  AGENTS.md  ${GREEN}(AI agent entry point)${NC}"
echo ""
echo -e "${BOLD}Learn more:${NC} ${CYAN}https://github.com/ChahatUpadhyay/LoopSpec${NC}"
echo ""
