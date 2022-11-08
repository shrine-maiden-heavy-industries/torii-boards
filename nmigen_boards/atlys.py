from torii_boards.atlys import *
from torii_boards.atlys import __all__


import warnings
warnings.warn("instead of nmigen_boards.atlys, use amaranth_boards.atlys",
              DeprecationWarning, stacklevel=2)
