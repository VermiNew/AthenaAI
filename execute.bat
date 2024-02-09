@echo off
set "venv_dir=.venv"

if not exist %venv_dir% (
    echo Creating virtual environment...
    python -m venv %venv_dir%
)

echo Calling activation script...
call %venv_dir%\Scripts\activate

:check
@echo on
echo If text named .venv is visible then everything is good.
@echo off

:install_libraries
echo Do you want to install the required libraries? (y/n)
set /p install_libraries_choice=

if /i "%install_libraries_choice%"=="y" (
    echo Calling library installer...
    echo Press ENTER to continue.
    pause >nul
    pip install -r requirements.txt

    if %errorlevel% neq 0 (
        echo Error installing requirements. Exiting...
        exit /b 1
    )

    echo Requirements installed!
) else if /i "%install_libraries_choice%"=="n" (
    echo Skipping library installation.
) else (
    echo Invalid choice. Please enter 'y' or 'n'.
    goto install_libraries
)

.\.venv\Scripts\python.exe -m pip install --upgrade pip

echo Console ready!

echo Initializing the main process...
call py startup.py --tags main
call py cleanup.py
