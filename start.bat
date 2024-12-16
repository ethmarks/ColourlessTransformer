@echo off

:: Activate virtual environment
if not exist "venv" (
    echo Virtual environment not found. Please run install.bat first.
    exit /b 1
)

call venv\Scripts\activate

:: Run the Python application
if exist "app.py" (
    echo Running app.py...
    python app.py
) else (
    echo app.py not found! Make sure the script exists in the directory.
    exit /b 1
)
