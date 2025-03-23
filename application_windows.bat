@echo off
setlocal enabledelayedexpansion

echo Checking if Python is installed...

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Installing Python...
    
    :: Download Python installer
    curl -o python_installer.exe https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe
    
    :: Install Python silently, with pip, add to PATH
    python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1
    
    :: Clean up installer
    del python_installer.exe
    
    echo Python has been installed.
) else (
    echo Python is already installed.
)

:: Check if requirements.txt exists
if not exist requirements.txt (
    echo Error: requirements.txt file not found.
    echo Please make sure the requirements.txt file is in the same directory as this batch file.
    pause
    exit /b 1
)

echo Installing dependencies from requirements.txt...
pip install -r requirements.txt

echo Dependencies installed. Starting application...

:: pip list

python ./src/app.py
echo Application closed.
pause