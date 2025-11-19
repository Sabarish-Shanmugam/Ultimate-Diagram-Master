@echo off
echo ========================================================
echo Ultimate Diagram Master - Setup and Run
echo ========================================================

REM Ensure we are running from the script's directory
cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python 3.11+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if venv exists, create if not
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate venv
call venv\Scripts\activate

REM Install dependencies
echo Installing/Updating dependencies...
pip install -r requirements.txt
pip install processpiper

REM Initialize project if config missing
if not exist "config\project_requirements.yaml" (
    echo Initializing project configuration...
    python src\pipeline_controller.py init
)

REM Run the pipeline
echo.
echo Running Diagram Generation Pipeline...
python src\pipeline_controller.py run

echo.
echo ========================================================
echo Done! Check the 'generated_diagrams' folder.
echo ========================================================
pause
