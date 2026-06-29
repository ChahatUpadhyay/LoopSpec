#Requires -Version 5.1
<#
.SYNOPSIS
    LoopSpec Bootstrap — PowerShell (cross-platform)
.DESCRIPTION
    Initializes a .loopspec/ directory in the target project with all
    template files, creates iterations/ subdirectory, and generates
    an AGENTS.md entry-point at the project root.
.PARAMETER TargetDir
    Path to the project to initialize. Defaults to the current directory.
.LINK
    https://github.com/loopspec/loopspec
#>

param(
    [Parameter(Position = 0)]
    [string]$TargetDir = "."
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# ── Resolve paths ────────────────────────────────────────────────────
$ScriptDir    = Split-Path -Parent $MyInvocation.MyCommand.Definition
$TemplateDir  = Join-Path $ScriptDir "templates"
$TargetDir    = Resolve-Path -Path $TargetDir -ErrorAction SilentlyContinue |
                Select-Object -ExpandProperty Path
if (-not $TargetDir) { $TargetDir = $PWD.Path }

$LoopSpecDir  = Join-Path $TargetDir ".loopspec"
$IterationsDir = Join-Path $LoopSpecDir "iterations"
$AgentsFile   = Join-Path $TargetDir "AGENTS.md"

# ── Preflight checks ────────────────────────────────────────────────
if (-not (Test-Path $TemplateDir -PathType Container)) {
    Write-Host "✗ Error: " -ForegroundColor Red -NoNewline
    Write-Host "templates/ directory not found at $TemplateDir"
    Write-Host "  Make sure you run this script from the LoopSpec installation directory."
    exit 1
}

if (Test-Path $LoopSpecDir -PathType Container) {
    Write-Host "⚠ Warning: " -ForegroundColor Yellow -NoNewline
    Write-Host ".loopspec/ already exists in $TargetDir"
    Write-Host "  To avoid overwriting your existing configuration, this script will exit."
    Write-Host "  Remove .loopspec/ manually if you want to re-initialize."
    exit 1
}

# ── Create directory structure ───────────────────────────────────────
Write-Host "▸ " -ForegroundColor Blue -NoNewline
Write-Host "Creating .loopspec/ directory structure..."
New-Item -ItemType Directory -Path $IterationsDir -Force | Out-Null

# ── Copy template files ─────────────────────────────────────────────
Write-Host "▸ " -ForegroundColor Blue -NoNewline
Write-Host "Copying template files..."

$templates = Get-ChildItem -Path $TemplateDir -Filter "*.md" -File -ErrorAction SilentlyContinue
if (-not $templates -or $templates.Count -eq 0) {
    Write-Host "✗ Error: " -ForegroundColor Red -NoNewline
    Write-Host "No .md template files found in $TemplateDir"
    Remove-Item -Path $LoopSpecDir -Recurse -Force -ErrorAction SilentlyContinue
    exit 1
}

foreach ($tmpl in $templates) {
    Copy-Item -Path $tmpl.FullName -Destination $LoopSpecDir -Force
}

Write-Host "  ✓ " -ForegroundColor Green -NoNewline
Write-Host "Copied $($templates.Count) template files"

# ── Generate AGENTS.md at project root ───────────────────────────────
Write-Host "▸ " -ForegroundColor Blue -NoNewline
Write-Host "Generating AGENTS.md at project root..."

$agentsContent = @"
# AGENTS.md

> This project uses [LoopSpec](https://github.com/loopspec/loopspec) — a self-correcting AI development protocol.

## Instructions for AI Agents

Before making any changes to this project, read and follow the LoopSpec protocol:

1. **Read** ``.loopspec/PROTOCOL.md`` for the complete operating manual
2. **Read** ``.loopspec/GOAL.md`` for the current objective and success criteria
3. **Read** ``.loopspec/STATUS.md`` for the current execution state
4. **Read** ``.loopspec/LEARNINGS.md`` for past mistakes to avoid

Follow the LoopSpec phases: ANALYZE → PLAN → TEST → IMPLEMENT → VERIFY → EVALUATE

Do not skip phases. Do not proceed without human approval on PLAN.md.
"@

Set-Content -Path $AgentsFile -Value $agentsContent -Encoding UTF8

Write-Host "  ✓ " -ForegroundColor Green -NoNewline
Write-Host "AGENTS.md created"

# ── Success banner ───────────────────────────────────────────────────
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green
Write-Host "  ✓ LoopSpec initialized successfully!" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green
Write-Host ""

Write-Host "Getting started:" -ForegroundColor White
Write-Host ""
Write-Host "  1. " -ForegroundColor Cyan -NoNewline
Write-Host "Define your goal and success criteria:"
Write-Host "     " -NoNewline
Write-Host "code .loopspec/GOAL.md" -ForegroundColor Yellow
Write-Host ""
Write-Host "  2. " -ForegroundColor Cyan -NoNewline
Write-Host "Open the project with your AI coding tool"
Write-Host ""
Write-Host "  3. " -ForegroundColor Cyan -NoNewline
Write-Host "Tell the AI to read the protocol:"
Write-Host "     " -NoNewline
Write-Host '"Read .loopspec/PROTOCOL.md and begin."' -ForegroundColor Yellow
Write-Host ""

Write-Host "Directory layout:" -ForegroundColor White
Write-Host ""
Write-Host "  .loopspec/" -ForegroundColor Blue
$copiedFiles = Get-ChildItem -Path $LoopSpecDir -Filter "*.md" -File
foreach ($f in $copiedFiles) {
    Write-Host "  ├── $($f.Name)"
}
Write-Host "  └── iterations/" -ForegroundColor Blue
Write-Host ""
Write-Host "  AGENTS.md  " -NoNewline
Write-Host "(auto-generated — AI agent entry point)" -ForegroundColor Green
Write-Host ""
Write-Host "Learn more: " -NoNewline
Write-Host "https://github.com/loopspec/loopspec" -ForegroundColor Cyan
Write-Host ""
