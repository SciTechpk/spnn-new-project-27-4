@echo off
echo Updating Python scripts...

:: Update all Python scripts
for %%f in (*.py) do (
    echo Updating %%f...
    python %%f
)

echo All scripts updated successfully.
pause