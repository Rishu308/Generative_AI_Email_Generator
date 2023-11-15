@echo off
setlocal

REM Define the name of the virtual environment
set VENV_NAME=my_venv

REM Create the virtual environment
python -m venv %VENV_NAME%

REM Activate the virtual environment
call %VENV_NAME%\Scripts\activate

REM Install the required modules
pip install pyimgur openai tensorflow opencv-python jinja2 requests

REM Run Python script
python main.py

REM Pause the script to keep the command prompt window open
pause

REM Open the browser
echo Opening browser...
start "" http://127.0.0.1:5000

REM Deactivate the virtual environment
deactivate

endlocal
