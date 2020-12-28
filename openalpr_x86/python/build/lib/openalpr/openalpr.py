import ctypes
import json
import os
import platform
import sys


class Alpr():
    def __init__(self, country, config_file, runtime_dir):

        from pathlib import Path

        def find_data_file():
            print("frozen ++++ " + str(getattr(sys, 'frozen', False)))
            if getattr(sys, 'frozen', False):
                # The application is frozen
                datadir = Path.joinpath(Path(os.path.dirname(sys.executable)).resolve(), 'openalpr_x86')
            else:
                # The application is not frozen
                # Change this bit to match where you store your data files:
                datadir = Path(__file__).parent.parent.parent.parent.parent
            print("=================== "+str(datadir))
            return datadir

        OPENALPR_PATH = find_data_file()

        # Load the .dll for Windows and the .so for Unix-based
        if platform.system().lower().find("windows") != -1:
            self._openalprpy_lib = ctypes.cdll.LoadLibrary(str(Path.joinpath(OPENALPR_PATH, "openalprpy.dll")))
        elif platform.system().lower().find("darwin") != -1:
            self._openalprpy_lib = ctypes.cdll.LoadLibrary(str(Path.joinpath(OPENALPR_PATH, "libopenalprpy.dylib")))
        else:
            self._openalprpy_lib = ctypes.cdll.LoadLibrary(str(Path.joinpath(OPENALPR_PATH, "libopenalprpy.so")))

        # print("1::::::")
        self._initialize_func = self._openalprpy_lib.initialize
        self._initialize_func.restype = ctypes.c_void_p
        self._initialize_func.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]

        # print("2::::::")
        self._dispose_func = self._openalprpy_lib.dispose
        self._dispose_func.argtypes = [ctypes.c_void_p]

        # print("3::::::")
        self._is_loaded_func = self._openalprpy_lib.isLoaded
        self._is_loaded_func.argtypes = [ctypes.c_void_p]
        self._is_loaded_func.restype = ctypes.c_bool

        # print("4::::::")
        self._recognize_file_func = self._openalprpy_lib.recognizeFile
        self._recognize_file_func.restype = ctypes.c_void_p
        self._recognize_file_func.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

        # print("5::::::")
        self._recognize_array_func = self._openalprpy_lib.recognizeArray
        self._recognize_array_func.restype = ctypes.c_void_p
        self._recognize_array_func.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_uint]

        self._free_json_mem_func = self._openalprpy_lib.freeJsonMem

        # print("6::::::")
        self._set_default_region_func = self._openalprpy_lib.setDefaultRegion
        self._set_default_region_func.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

        # print("7::::::")
        self._set_detect_region_func = self._openalprpy_lib.setDetectRegion
        self._set_detect_region_func.argtypes = [ctypes.c_void_p, ctypes.c_bool]

        # print("8::::::")
        self._set_top_n_func = self._openalprpy_lib.setTopN
        self._set_top_n_func.argtypes = [ctypes.c_void_p, ctypes.c_int]

        # print("9::::::")
        self._get_version_func = self._openalprpy_lib.getVersion
        self._get_version_func.argtypes = [ctypes.c_void_p]
        self._get_version_func.restype = ctypes.c_void_p

        # print("10::::::")
        self.alpr_pointer = self._initialize_func(country, config_file, runtime_dir)
        print("11::::::")

    def unload(self):
        self._openalprpy_lib.dispose(self.alpr_pointer)

    def is_loaded(self):
        return self._is_loaded_func(self.alpr_pointer)

    def recognize_file(self, file_path):
        ptr = self._recognize_file_func(self.alpr_pointer, file_path)
        json_data = ctypes.cast(ptr, ctypes.c_char_p).value
        response_obj = json.loads(json_data)
        self._free_json_mem_func(ctypes.c_void_p(ptr))

        return response_obj

    def recognize_array(self, byte_array):
        # print("12::::::")
        pb = ctypes.cast(byte_array, ctypes.POINTER(ctypes.c_ubyte))
        ptr = self._recognize_array_func(self.alpr_pointer, pb, len(byte_array))
        json_data = ctypes.cast(ptr, ctypes.c_char_p).value
        response_obj = json.loads(json_data)
        self._free_json_mem_func(ctypes.c_void_p(ptr))

        return response_obj

    def get_version(self):

        ptr = self._get_version_func(self.alpr_pointer)
        version_number = ctypes.cast(ptr, ctypes.c_char_p).value
        self._free_json_mem_func(ctypes.c_void_p(ptr))

        return version_number

    def set_top_n(self, topn):
        self._set_top_n_func(self.alpr_pointer, topn)

    def set_default_region(self, region):
        self._set_default_region_func(self.alpr_pointer, region)

    def set_detect_region(self, enabled):
        self._set_detect_region_func(self.alpr_pointer, enabled)


