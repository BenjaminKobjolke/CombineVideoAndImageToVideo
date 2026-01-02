@echo off
echo Checking for uv installation...
where uv >nul 2>&1
if errorlevel 1 (
    echo uv is not installed. Please install it first:
    echo   https://docs.astral.sh/uv/getting-started/installation/
    pause
    exit /b 1
)
echo.

echo Installing dependencies with uv...
uv sync --all-extras
echo.

echo Verifying installation...
uv run python -c "import cv2; import numpy; print('Dependencies installed successfully!')"
echo.

echo Installation complete! You can now:
echo 1. Run the tool with: start.bat --help
echo 2. Run tests with: tools\tests.bat
echo.

pause
