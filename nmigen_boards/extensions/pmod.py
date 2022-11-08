from torii_boards.extensions.pmod import *
from torii_boards.extensions.pmod import __all__


import warnings
warnings.warn("instead of nmigen_boards.extensions.pmod, use amaranth_boards.extensions.pmod",
              DeprecationWarning, stacklevel=2)
