@echo off
echo Creating Python virtual environment...
python -m venv venv
echo.

echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo Installing requirements...
pip install -r requirements.txt
echo.

echo Installation complete! You can now:
echo 1. Run 'activate_environment.bat' to activate the virtual environment
echo 2. Use the script with: python combine_video_image.py --help
echo.

pause
