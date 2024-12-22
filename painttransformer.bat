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
echo Resizing and processing file: %INPUT_FILE%
echo.

:: Resize the image to a max of 512 pixels using Python and save it to a temp path
python -c "from PIL import Image; import os; \
input_path = r'%INPUT_FILE%'; \
output_path = os.path.join(os.path.dirname(input_path), 'temp_resized.png'); \
image = Image.open(input_path); \
max_dim = 512; \
resize_ratio = min(max_dim / image.width, max_dim / image.height) if image.width > max_dim or image.height > max_dim else 1; \
new_size = (int(image.width * resize_ratio), int(image.height * resize_ratio)); \
image.resize(new_size, Image.LANCZOS).save(output_path); \
print(f'Resized image saved to {output_path}')"

:: Check if the resized file exists
if not exist "%~dp0temp_resized.png" (
    echo Failed to resize image: %INPUT_FILE%.
    echo.
    exit /b
)

:: Run the Python script with the resized file
python -c "from inference.inference import main; main(input_path=r'%~dp0temp_resized.png', model_path=r'inference/model.pth', output_dir=r'inference/output/', need_animation=False, serial=False)"

:: Check the exit status of Python
if %errorlevel% neq 0 (
    echo Failed to process: %INPUT_FILE%.
    echo.
    exit /b
) else (
    echo Successfully processed: %INPUT_FILE%.
    echo.
)

:: Delete the temporary resized image
del "%~dp0temp_resized.png"

:: Commit changes with a message
:: Ensure Git is initialized and configured in the directory
git add inference/output/*
git commit -m "feat: Processed and resized image %~nI"
exit /b
