@echo off
:: Check if at least one argument (image file) is passed
if "%~1"=="" (
    echo Drag and drop image files onto this batch file to process them.
    pause
    exit /b
)

:: Iterate over all dropped files
for %%I in (%*) do (
    :: Ensure the file has a valid image extension
    if /i "%%~xI"==".jpg" (call :PROCESS_FILE "%%~fI")
    if /i "%%~xI"==".jpeg" (call :PROCESS_FILE "%%~fI")
    if /i "%%~xI"==".png" (call :PROCESS_FILE "%%~fI")
)

exit /b

:PROCESS_FILE
:: Set up variables
set "INPUT_FILE=%~1"

:: Run the Python script with the input file
python -c "from inference.inference import main; main(input_path='%INPUT_FILE%', model_path='inference/model.pth', output_dir='inference/output/', need_animation=False, serial=False)"

:: Check the exit status of Python
if %errorlevel% neq 0 (
    echo Failed to process %INPUT_FILE%.
    pause
    exit /b
) else (
    echo Successfully processed %INPUT_FILE%.
)

exit /b
