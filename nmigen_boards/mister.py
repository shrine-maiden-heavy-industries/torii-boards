from torii_boards.mister import *
from torii_boards.mister import __all__


import warnings
warnings.warn("instead of nmigen_boards.mister, use amaranth_boards.mister",
              DeprecationWarning, stacklevel=2)
