from cx_Freeze import setup, Executable

options = {
    'build_exe': 'build_core'
}

include_files = ['openalpr_x86', 'config.toml']

setup(name="test02",
      version="0.1",
      description="My GUI application!",
      options={'build_exe': {'include_files': include_files}},
      executables=[Executable("mainCore.py")])
