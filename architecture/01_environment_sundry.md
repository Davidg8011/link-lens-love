# Architectural SOP: Environment Requirements

## Layer 3 Engines (Python Environments)
- **Constraint Discovered:** The Windows default "App execution aliases" redirect `python` or `python3` to the MS Store installer. 
- **Solution Discovered:** Python is available via Thonny IDE at `C:/Users/David/AppData/Local/Programs/Thonny/python.exe`.
- **SOP canonical run command:**
  ```powershell
  $env:PYTHONIOENCODING="utf-8"; & "C:/Users/David/AppData/Local/Programs/Thonny/python.exe" tools/<script_name>.py
  ```
  *(The `PYTHONIOENCODING=utf-8` flag ensures emoji characters in script logs don't crash the cp1252 Windows terminal).*

*Stored learning based on initialization and user-provided fix on 2026-03-18.*
