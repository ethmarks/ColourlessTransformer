@echo off
:: Change to the directory where the batch file is located
cd /d "%~dp0"

:: Activate virtual environment
if not exist "venv" (
    echo Virtual environment not found. Please run install.bat first.
    exit /b 1
)

call venv\Scripts\activate

:: Check if at least one argument (image file) is passed
if "%~1"=="" (
    echo Drag and drop image files onto this batch file to process them.
    echo.
    echo Usage:
    echo   - Drag and drop images to process as static images
    echo   - Use --animation flag for animated output: painttransformer.bat image.jpg --animation
    echo   - Use --no-resize flag to skip resizing: painttransformer.bat image.jpg --no-resize
    pause
    exit /b
)

:: Check for animation and no-resize flags
set "ANIMATION_FLAG="
set "NO_RESIZE_FLAG="
for %%i in (%*) do (
    if /i "%%i"=="--animation" set "ANIMATION_FLAG=--animation"
    if /i "%%i"=="--no-resize" set "NO_RESIZE_FLAG=--no-resize"
)

:: Inform the user of the starting process
echo Starting image processing...
if defined ANIMATION_FLAG echo Animation mode enabled.
if defined NO_RESIZE_FLAG echo No-resize mode enabled.
echo This may take some time depending on the number of images and their sizes.
echo.

:: Iterate over all dropped files
for %%I in (%*) do (
    :: Skip the flag parameters
    if /i not "%%I"=="--animation" (
        if /i not "%%I"=="--no-resize" (
            :: Ensure the file has a valid image extension
            if /i "%%~xI"==".jpg" (call :PROCESS_FILE "%%~fI")
            if /i "%%~xI"==".jpeg" (call :PROCESS_FILE "%%~fI")
            if /i "%%~xI"==".png" (call :PROCESS_FILE "%%~fI")
        )
    )
)

echo.
echo All image processing tasks completed.
pause
exit /b

:PROCESS_FILE
:: Set up variables
set "INPUT_FILE=%~1"

:: Notify which file is being processed
echo Resizing and processing file: %INPUT_FILE%
echo.

:: Call the Python script to resize and process the image
python colourlesstransformer.py "%INPUT_FILE%" %ANIMATION_FLAG% %NO_RESIZE_FLAG%

:: Check the exit status of Python
if %errorlevel% neq 0 (
    echo Failed to process: %INPUT_FILE%.
    echo.
    exit /b
) else (
    echo Successfully processed: %INPUT_FILE%.
    echo.
)
