@echo off
REM Activate the virtual environment and run main.py

REM Go to project directory
cd /d "%~dp0"

REM Activate venv
call venv\Scripts\activate.bat

REM Run the Python script
python bgr_file_sorter.py

REM Pause to keep window open if script exits
pause
