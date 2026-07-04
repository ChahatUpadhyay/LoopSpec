@echo off
setlocal enabledelayedexpansion
:: LoopSpec v2 Bootstrap - Windows CMD
:: https://github.com/ChahatUpadhyay/LoopSpec
:: NOTE: This file uses ASCII-only characters to avoid CMD parsing errors.

:: -- Resolve paths ----------------------------------------------------
set "SCRIPT_DIR=%~dp0"
set "TEMPLATE_DIR=%SCRIPT_DIR%templates"
set "REPAIR_MODE=0"

:: Parse arguments
set "TARGET_DIR=."
:parse_args
if "%~1"=="" goto :done_args
if /i "%~1"=="--repair" (set "REPAIR_MODE=1" & shift & goto :parse_args)
if /i "%~1"=="--upgrade" (set "REPAIR_MODE=1" & shift & goto :parse_args)
set "TARGET_DIR=%~1"
shift
goto :parse_args
:done_args

set "LOOPSPEC_DIR=%TARGET_DIR%\.loopspec"
set "ITERATIONS_DIR=%LOOPSPEC_DIR%\iterations"
set "AGENTS_FILE=%TARGET_DIR%\AGENTS.md"

:: -- Validate target directory ----------------------------------------
if not exist "%TARGET_DIR%\" (
    echo [ERROR] Target directory does not exist: %TARGET_DIR%
    exit /b 1
)

:: -- Preflight checks -------------------------------------------------
if not exist "%TEMPLATE_DIR%\" (
    echo [ERROR] templates\ directory not found at %TEMPLATE_DIR%
    echo         Make sure you run this script from the LoopSpec installation directory.
    exit /b 1
)

if exist "%LOOPSPEC_DIR%\" (
    if "%REPAIR_MODE%"=="0" (
        echo [WARNING] .loopspec\ already exists in %TARGET_DIR%
        echo           Use --repair to update protocol files without overwriting your data.
        exit /b 1
    )
)

:: -- Create directory structure ---------------------------------------
echo [*] Creating .loopspec\ directory structure...
if not exist "%ITERATIONS_DIR%\" mkdir "%ITERATIONS_DIR%"

:: -- Copy template files ----------------------------------------------
echo [*] Copying template files...
set COPIED=0
set SKIPPED=0

for %%F in ("%TEMPLATE_DIR%\*.md" "%TEMPLATE_DIR%\*.json") do (
    if "%REPAIR_MODE%"=="1" (
        if exist "%LOOPSPEC_DIR%\%%~nxF" (
            if /i "%%~nxF"=="PROTOCOL.md" (
                copy /y "%%F" "%LOOPSPEC_DIR%\" >nul
                set /a COPIED+=1
            ) else if /i "%%~nxF"=="STATUS.json" (
                copy /y "%%F" "%LOOPSPEC_DIR%\" >nul
                set /a COPIED+=1
            ) else (
                set /a SKIPPED+=1
            )
        ) else (
            copy /y "%%F" "%LOOPSPEC_DIR%\" >nul
            set /a COPIED+=1
        )
    ) else (
        copy /y "%%F" "%LOOPSPEC_DIR%\" >nul
        set /a COPIED+=1
    )
)

if !COPIED! equ 0 if !SKIPPED! equ 0 (
    echo [ERROR] No template files found in %TEMPLATE_DIR%
    if "%REPAIR_MODE%"=="0" rmdir /s /q "%LOOPSPEC_DIR%" 2>nul
    exit /b 1
)

echo     [OK] Copied !COPIED! files, skipped !SKIPPED! (preserved)

:: -- Handle AGENTS.md (non-destructive) -------------------------------
if exist "%AGENTS_FILE%" (
    findstr /i "LoopSpec" "%AGENTS_FILE%" >nul 2>&1
    if !errorlevel! equ 0 (
        echo     [OK] AGENTS.md already contains LoopSpec instructions (skipped)
    ) else (
        echo [*] Appending LoopSpec instructions to existing AGENTS.md...
        echo.>> "%AGENTS_FILE%"
        echo --->> "%AGENTS_FILE%"
        echo.>> "%AGENTS_FILE%"
        call :write_agents_content "%AGENTS_FILE%"
        echo     [OK] LoopSpec instructions appended
    )
) else (
    echo [*] Creating AGENTS.md at project root...
    call :write_agents_content "%AGENTS_FILE%"
    echo     [OK] AGENTS.md created
)

:: -- Success banner ---------------------------------------------------
echo.
echo ================================================
echo   LoopSpec v2 initialized successfully!
echo ================================================
echo.
echo Getting started:
echo.
echo   1. Define your goal and success criteria:
echo      notepad .loopspec\GOAL.md
echo.
echo   2. Open the project with your AI coding tool
echo.
echo   3. Tell the AI:
echo      "Read .loopspec/PROTOCOL.md and begin."
echo.
echo Directory layout:
echo.
echo   .loopspec\
for %%F in ("%LOOPSPEC_DIR%\*.md" "%LOOPSPEC_DIR%\*.json") do (
    echo   +-- %%~nxF
)
echo   +-- iterations\
echo.
echo   AGENTS.md  (AI agent entry point)
echo.
echo Learn more: https://github.com/ChahatUpadhyay/LoopSpec
echo.

endlocal
exit /b 0

:: -- Subroutine: Write AGENTS.md content ------------------------------
:write_agents_content
(
echo # AGENTS.md
echo.
echo ^> This project uses [LoopSpec v2](https://github.com/ChahatUpadhyay/LoopSpec) - a self-correcting, evidence-driven AI development protocol.
echo.
echo ## Instructions for AI Agents
echo.
echo Before making any changes to this project, read and follow the LoopSpec protocol:
echo.
echo 1. **Read** `.loopspec/PROTOCOL.md` for the complete operating manual
echo 2. **Read** `.loopspec/GOAL.md` for the current objective and success criteria
echo 3. **Read** `.loopspec/STATUS.md` or `.loopspec/STATUS.json` for execution state
echo 4. **Read** `.loopspec/LEARNINGS.md` for past mistakes to avoid
echo.
echo Follow the LoopSpec phases: ANALYZE ^> PLAN ^> TEST ^> IMPLEMENT ^> VERIFY ^> ADVERSARIAL ^> EVALUATE
echo.
echo Do not skip phases. Do not proceed without human approval on PLAN.md.
echo Do not weaken tests or thresholds to pass criteria.
) > %1
exit /b 0
