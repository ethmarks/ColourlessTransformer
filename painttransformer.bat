@echo off
:: Change to the directory where the batch file is located
cd /d "%~dp0"

:: Check if at least one argument (image file) is passed
if "%~1"=="" (
    echo Drag and drop image files onto this batch file to process them.
    pause
    exit /b
)

:: Inform the user of the starting process
echo Starting image processing...
echo This may take some time depending on the number of images and their sizes.
echo.

:: Iterate over all dropped files
for %%I in (%*) do (
    :: Ensure the file has a valid image extension
    if /i "%%~xI"==".jpg" (call :PROCESS_FILE "%%~fI")
    if /i "%%~xI"==".jpeg" (call :PROCESS_FILE "%%~fI")
    if /i "%%~xI"==".png" (call :PROCESS_FILE "%%~fI")
)

echo.
echo All image processing tasks completed.
pause
exit /b

:PROCESS_FILE
:: Set up variables
set "INPUT_FILE=%~1"

:: Notify which file is being processed
echo Processing file: %INPUT_FILE%
echo.

:: Run the Python script with the input file, using raw string literals for paths
python -c "import time; print('Running inference...'); time.sleep(2); from inference.inference import main; main(input_path=r'%INPUT_FILE%', model_path=r'inference/model.pth', output_dir=r'inference/output/', need_animation=False, serial=False)"

:: Check the exit status of Python
if %errorlevel% neq 0 (
    echo Failed to process: %INPUT_FILE%.
    echo.
    exit /b
) else (
    echo Successfully processed: %INPUT_FILE%.
    echo.
)

:: Commit changes with a message
:: Ensure Git is initialized and configured in the directory
git add inference/output/*
git commit -m "feat: Processed image %~nI"
exit /b
