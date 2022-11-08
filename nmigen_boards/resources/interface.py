from torii_boards.resources.interface import *
from torii_boards.resources.interface import __all__


import warnings
warnings.warn("instead of nmigen_boards.resources.interface, use amaranth_boards.resources.interface",
              DeprecationWarning, stacklevel=2)
