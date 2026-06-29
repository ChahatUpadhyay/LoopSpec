@echo off
setlocal enabledelayedexpansion
:: LoopSpec Bootstrap — Windows CMD
:: https://github.com/loopspec/loopspec

:: ── Resolve paths ────────────────────────────────────────────────────
set "SCRIPT_DIR=%~dp0"
set "TEMPLATE_DIR=%SCRIPT_DIR%templates"
if "%~1"=="" (set "TARGET_DIR=.") else (set "TARGET_DIR=%~1")
set "LOOPSPEC_DIR=%TARGET_DIR%\.loopspec"
set "ITERATIONS_DIR=%LOOPSPEC_DIR%\iterations"
set "AGENTS_FILE=%TARGET_DIR%\AGENTS.md"

:: ── Preflight checks ────────────────────────────────────────────────
if not exist "%TEMPLATE_DIR%\" (
    echo [ERROR] templates\ directory not found at %TEMPLATE_DIR%
    echo         Make sure you run this script from the LoopSpec installation directory.
    exit /b 1
)

if exist "%LOOPSPEC_DIR%\" (
    echo [WARNING] .loopspec\ already exists in %TARGET_DIR%
    echo           To avoid overwriting your existing configuration, this script will exit.
    echo           Remove .loopspec\ manually if you want to re-initialize.
    exit /b 1
)

:: ── Create directory structure ───────────────────────────────────────
echo [*] Creating .loopspec\ directory structure...
mkdir "%ITERATIONS_DIR%" 2>nul

:: ── Copy template files ─────────────────────────────────────────────
echo [*] Copying template files...
set COPIED=0
for %%F in ("%TEMPLATE_DIR%\*.md") do (
    copy /y "%%F" "%LOOPSPEC_DIR%\" >nul
    set /a COPIED+=1
)

if %COPIED% equ 0 (
    echo [ERROR] No .md template files found in %TEMPLATE_DIR%
    rmdir /s /q "%LOOPSPEC_DIR%" 2>nul
    exit /b 1
)

echo     [OK] Copied %COPIED% template files

:: ── Generate AGENTS.md at project root ───────────────────────────────
echo [*] Generating AGENTS.md at project root...
(
echo # AGENTS.md
echo.
echo ^> This project uses [LoopSpec](https://github.com/loopspec/loopspec) — a self-correcting AI development protocol.
echo.
echo ## Instructions for AI Agents
echo.
echo Before making any changes to this project, read and follow the LoopSpec protocol:
echo.
echo 1. **Read** `.loopspec/PROTOCOL.md` for the complete operating manual
echo 2. **Read** `.loopspec/GOAL.md` for the current objective and success criteria
echo 3. **Read** `.loopspec/STATUS.md` for the current execution state
echo 4. **Read** `.loopspec/LEARNINGS.md` for past mistakes to avoid
echo.
echo Follow the LoopSpec phases: ANALYZE → PLAN → TEST → IMPLEMENT → VERIFY → EVALUATE
echo.
echo Do not skip phases. Do not proceed without human approval on PLAN.md.
) > "%AGENTS_FILE%"
echo     [OK] AGENTS.md created

:: ── Success banner ───────────────────────────────────────────────────
echo.
echo ======================================================
echo   [OK] LoopSpec initialized successfully!
echo ======================================================
echo.
echo Getting started:
echo.
echo   1. Define your goal and success criteria:
echo      notepad .loopspec\GOAL.md
echo.
echo   2. Open the project with your AI coding tool
echo.
echo   3. Tell the AI to read the protocol:
echo      "Read .loopspec/PROTOCOL.md and begin."
echo.
echo Directory layout:
echo.
echo   .loopspec\
for %%F in ("%LOOPSPEC_DIR%\*.md") do (
    echo   +-- %%~nxF
)
echo   +-- iterations\
echo.
echo   AGENTS.md  (auto-generated — AI agent entry point)
echo.
echo Learn more: https://github.com/loopspec/loopspec
echo.

endlocal
