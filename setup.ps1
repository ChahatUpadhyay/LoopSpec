#Requires -Version 5.1
<#
.SYNOPSIS
    LoopSpec v2 Bootstrap - PowerShell (cross-platform)
.DESCRIPTION
    Initializes a .loopspec/ directory in the target project with all
    template files, creates iterations/ subdirectory, and generates
    an AGENTS.md entry-point at the project root.
    Supports -Repair mode to upgrade without overwriting user data.
.PARAMETER TargetDir
    Path to the project to initialize. Defaults to the current directory.
.PARAMETER Repair
    Update protocol files without overwriting user data files.
.LINK
    https://github.com/ChahatUpadhyay/LoopSpec
#>

param(
    [Parameter(Position = 0)]
    [string]$TargetDir = ".",
    [switch]$Repair
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# -- Resolve paths -----------------------------------------------------
$ScriptDir    = Split-Path -Parent $MyInvocation.MyCommand.Definition
$TemplateDir  = Join-Path $ScriptDir "templates"

# Validate and resolve target directory
if (-not (Test-Path $TargetDir -PathType Container)) {
    Write-Host "[ERROR] " -ForegroundColor Red -NoNewline
    Write-Host "Target directory does not exist: $TargetDir"
    exit 1
}
$TargetDir = (Resolve-Path -Path $TargetDir).Path

$LoopSpecDir   = Join-Path $TargetDir ".loopspec"
$IterationsDir = Join-Path $LoopSpecDir "iterations"
$AgentsFile    = Join-Path $TargetDir "AGENTS.md"

# -- Preflight checks --------------------------------------------------
if (-not (Test-Path $TemplateDir -PathType Container)) {
    Write-Host "[ERROR] " -ForegroundColor Red -NoNewline
    Write-Host "templates/ directory not found at $TemplateDir"
    Write-Host "  Make sure you run this script from the LoopSpec installation directory."
    exit 1
}

if ((Test-Path $LoopSpecDir -PathType Container) -and (-not $Repair)) {
    Write-Host "[WARNING] " -ForegroundColor Yellow -NoNewline
    Write-Host ".loopspec/ already exists in $TargetDir"
    Write-Host "  Use -Repair to update protocol files without overwriting your data."
    exit 1
}

# -- Create directory structure ----------------------------------------
Write-Host "[*] " -ForegroundColor Blue -NoNewline
Write-Host "Creating .loopspec/ directory structure..."
New-Item -ItemType Directory -Path $IterationsDir -Force | Out-Null

# -- Copy template files -----------------------------------------------
Write-Host "[*] " -ForegroundColor Blue -NoNewline
Write-Host "Copying template files..."

$templates = Get-ChildItem -Path $TemplateDir -Include "*.md","*.json" -File -ErrorAction SilentlyContinue
if (-not $templates -or $templates.Count -eq 0) {
    # Try without -Include for PS 5.1 compatibility
    $templates = @()
    $templates += Get-ChildItem -Path $TemplateDir -Filter "*.md" -File -ErrorAction SilentlyContinue
    $templates += Get-ChildItem -Path $TemplateDir -Filter "*.json" -File -ErrorAction SilentlyContinue
}

if (-not $templates -or $templates.Count -eq 0) {
    Write-Host "[ERROR] " -ForegroundColor Red -NoNewline
    Write-Host "No template files found in $TemplateDir"
    if (-not $Repair) {
        Remove-Item -Path $LoopSpecDir -Recurse -Force -ErrorAction SilentlyContinue
    }
    exit 1
}

$copied = 0
$skipped = 0
foreach ($tmpl in $templates) {
    $dest = Join-Path $LoopSpecDir $tmpl.Name
    if ((Test-Path $dest) -and $Repair) {
        # In repair mode: only overwrite PROTOCOL.md and STATUS.json
        if ($tmpl.Name -eq "PROTOCOL.md" -or $tmpl.Name -eq "STATUS.json") {
            Copy-Item -Path $tmpl.FullName -Destination $dest -Force
            $copied++
        } else {
            $skipped++
        }
    } else {
        Copy-Item -Path $tmpl.FullName -Destination $LoopSpecDir -Force
        $copied++
    }
}

Write-Host "  [OK] " -ForegroundColor Green -NoNewline
Write-Host "Copied $copied files, skipped $skipped (preserved)"

# -- Handle AGENTS.md (non-destructive) --------------------------------
$agentsContent = @"
# AGENTS.md

> This project uses [LoopSpec v2](https://github.com/ChahatUpadhyay/LoopSpec) - a self-correcting, evidence-driven AI development protocol.

## Instructions for AI Agents

Before making any changes to this project, read and follow the LoopSpec protocol:

1. **Read** ``.loopspec/PROTOCOL.md`` for the complete operating manual
2. **Read** ``.loopspec/GOAL.md`` for the current objective and success criteria
3. **Read** ``.loopspec/STATUS.md`` or ``.loopspec/STATUS.json`` for execution state
4. **Read** ``.loopspec/LEARNINGS.md`` for past mistakes to avoid

Follow the LoopSpec phases: ANALYZE > PLAN > TEST > IMPLEMENT > VERIFY > ADVERSARIAL > EVALUATE

Do not skip phases. Do not proceed without human approval on PLAN.md.
Do not weaken tests or thresholds to pass criteria.
"@

if (Test-Path $AgentsFile) {
    $existingContent = Get-Content -Path $AgentsFile -Raw -ErrorAction SilentlyContinue
    if ($existingContent -and $existingContent.Contains("LoopSpec")) {
        Write-Host "  [OK] " -ForegroundColor Green -NoNewline
        Write-Host "AGENTS.md already contains LoopSpec instructions (skipped)"
    } else {
        Write-Host "[*] " -ForegroundColor Yellow -NoNewline
        Write-Host "Appending LoopSpec instructions to existing AGENTS.md..."
        Add-Content -Path $AgentsFile -Value "`n---`n`n$agentsContent" -Encoding UTF8
        Write-Host "  [OK] " -ForegroundColor Green -NoNewline
        Write-Host "LoopSpec instructions appended"
    }
} else {
    Write-Host "[*] " -ForegroundColor Blue -NoNewline
    Write-Host "Creating AGENTS.md at project root..."
    Set-Content -Path $AgentsFile -Value $agentsContent -Encoding UTF8
    Write-Host "  [OK] " -ForegroundColor Green -NoNewline
    Write-Host "AGENTS.md created"
}

# -- Success banner (ASCII-safe) ----------------------------------------
Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "  LoopSpec v2 initialized successfully!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
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
Write-Host "Tell the AI:"
Write-Host "     " -NoNewline
Write-Host '"Read .loopspec/PROTOCOL.md and begin."' -ForegroundColor Yellow
Write-Host ""

Write-Host "Directory layout:" -ForegroundColor White
Write-Host ""
Write-Host "  .loopspec/" -ForegroundColor Blue
$copiedFiles = Get-ChildItem -Path $LoopSpecDir -File
foreach ($f in $copiedFiles) {
    Write-Host "  |-- $($f.Name)"
}
Write-Host "  |-- iterations/" -ForegroundColor Blue
Write-Host ""
Write-Host "  AGENTS.md  " -NoNewline
Write-Host "(AI agent entry point)" -ForegroundColor Green
Write-Host ""
Write-Host "Learn more: " -NoNewline
Write-Host "https://github.com/ChahatUpadhyay/LoopSpec" -ForegroundColor Cyan
Write-Host ""
