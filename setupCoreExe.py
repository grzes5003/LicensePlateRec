from cx_Freeze import setup, Executable

options = {
    'build_exe': 'build_core'
}

include_files = ['openalpr_x86', 'config.toml']

setup(name="test02",
      version="0.2",
      description="LicensePlateRec!",
      options={'build_exe': {'include_files': include_files}},
      executables=[Executable("mainCore.py")])
