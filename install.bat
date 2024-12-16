@echo off

:: Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
) else (
    echo Virtual environment already exists.
)

:: Activate virtual environment
call venv\Scripts\activate

:: Install dependencies from requirements.txt
if exist "requirements.txt" (
    echo Installing dependencies from requirements.txt...
    pip install --upgrade pip
    pip install -r requirements.txt
) else (
    echo requirements.txt not found! Make sure it exists in the directory.
    exit /b 1
)

echo Setup complete! Use "run.bat" to execute the application.
