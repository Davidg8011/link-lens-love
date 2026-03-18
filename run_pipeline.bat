@echo off
echo ==========================================================
echo Starting B.L.A.S.T Pipeline: South Lake Tahoe Events
echo ==========================================================
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
"C:/Users/David/AppData/Local/Programs/Thonny/python.exe" tools/navigation.py
echo ==========================================================
echo Pipeline run successfully. Calendar has been updated!
echo ==========================================================
pause
