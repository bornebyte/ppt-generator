@echo off
REM PPT Generator CLI for Windows

set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM Check if virtual environment exists
if not exist "%SCRIPT_DIR%venv" (
    echo Error: Virtual environment not found.
    echo Please run install.bat first.
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Parse arguments
set "PRODUCTION=0"
set "PORT=5000"

if "%1"=="-p" (
    set "PRODUCTION=1"
    if not "%2"=="" (
        set "PORT=%2"
    )
)

if "%1"=="-h" goto :help
if "%1"=="--help" goto :help
if "%1"=="/?" goto :help

REM Start the server
if "%PRODUCTION%"=="1" (
    echo Starting PPT Generator in production mode on port %PORT%...
    echo Access the application at: http://localhost:%PORT%
    gunicorn -w 4 -b 0.0.0.0:%PORT% main:app
) else (
    echo Starting PPT Generator in development mode...
    echo Access the application at: http://localhost:5000
    set FLASK_APP=main.py
    set FLASK_ENV=development
    python main.py
)
exit /b 0

:help
echo PPT Generator CLI
echo.
echo Usage: pptgen.bat [OPTIONS]
echo.
echo Options:
echo   -p [port]    Run in production mode with Gunicorn (default port: 5000)
echo   -h           Show this help message
echo.
echo Examples:
echo   pptgen.bat              # Run development server
echo   pptgen.bat -p           # Run production server on port 5000
echo   pptgen.bat -p 8000      # Run production server on port 8000
exit /b 0
