import sys
print(getattr(sys, "base_prefix", None))
print(getattr(sys, "real_prefix", None))
print(getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix)

from core.manager.Manager import cli_entry

if __name__ == '__main__':
    cli_entry()
