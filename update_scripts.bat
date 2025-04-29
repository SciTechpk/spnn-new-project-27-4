@echo off
:: ================== SPNN Script Updater ==================
:: This batch file updates all Python scripts in the directory.

:: Step 1: Set working directory
cd /d D:\SPNN-New-Repo-27-4-2025\spnn-new-project-27-4 || (
    echo ❌ Failed to set working directory. Exiting...
    pause
    exit /b 1
)

:: Step 2: Update all Python scripts
echo 🔄 Updating Python scripts...

for %%f in (*.py) do (
    echo 📝 Updating %%f...
    py %%f || (
        echo ❌ Error running %%f
        pause
        exit /b 1
    )
)

:: Step 3: Notify completion
echo ✅ All Python scripts updated successfully.
pause