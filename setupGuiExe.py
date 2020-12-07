import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os", "toml", "rx", "opencv-python", "PySide2"], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

include_files = ['openalpr_x86', 'config.toml', 'gui']

setup(name="LicensePlateRecGUI",
      version="0.2",
      description="LicensePlateRec GUI!",
      options={'build_exe': {'include_files': include_files}},
      executables=[Executable("mainGui.py", base=base)])
