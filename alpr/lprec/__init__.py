import sys as _sys

if _sys.version_info.major >= 3:
    from .lprec import Alpr
else:
    from lprec import Alpr