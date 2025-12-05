@echo off
REM ============================================
REM PyPI Deployment Script
REM ============================================

echo.
echo ========================================
echo   HTTP Stub Server - PyPI Deployment
echo ========================================
echo.

REM Step 1: Clean old builds
echo [1/5] Cleaning old builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist http_stub_server.egg-info rmdir /s /q http_stub_server.egg-info
echo Done!
echo.

REM Step 2: Install/upgrade tools
echo [2/5] Installing build tools...
pip install --upgrade pip setuptools wheel twine
echo Done!
echo.

REM Step 3: Build package
echo [3/5] Building package...
python setup.py sdist bdist_wheel
echo Done!
echo.

REM Step 4: Check package
echo [4/5] Checking package...
twine check dist/*
echo Done!
echo.

REM Step 5: Upload
echo [5/5] Ready to upload!
echo.
echo Choose upload destination:
echo   1. Test PyPI (recommended first time)
echo   2. Real PyPI (production)
echo.
set /p choice="Enter choice (1 or 2): "

if "%choice%"=="1" (
    echo.
    echo Uploading to Test PyPI...
    twine upload --repository testpypi dist/*
) else if "%choice%"=="2" (
    echo.
    echo Uploading to Real PyPI...
    twine upload dist/*
) else (
    echo Invalid choice!
    exit /b 1
)

echo.
echo ========================================
echo   Deployment Complete!
echo ========================================
echo.
pause
