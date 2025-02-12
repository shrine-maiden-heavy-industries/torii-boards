# SPDX-License-Identifier: BSD-2-Clause

from torii.build                  import Connector
from torii.platform.vendor.xilinx import XilinxPlatform

__all__ = (
	'ZTurnLiteZ007SPlatform',
)

class ZTurnLiteZ007SPlatform(XilinxPlatform):
	device     = 'xc7z007s'
	package    = 'clg400'
	speed      = '1'

	pretty_name = 'Z-Turn Lite'
	description = 'Myir Z-Turn Lite Xilinx Zynq-7007 SoC Development Board'

	resources  = []
	connectors = [
		Connector('expansion', 0,
			'-   -   '
			'B19 E17 '
			'A20 D18 '
			'-   -   '
			'E18 D19 '
			'E19 D20 '
			'G17 F16 '
			'G18 F17 '
			'-   -   '
			'-   -   '
			'J18 J20 '
			'H18 H20 '
			'C20 K17 '
			'B20 K18 '
			'-   -   '
			'G19 K19 '
			'G20 J19 '
			'F19 H15 '
			'F20 G15 '
			'-   -   '
			'L16 K14 '
			'L17 J14 '
			'L19 H16 '
			'L20 H17 '
			'-   -   '
			'K16 L14 '
			'J16 L15 '
			'M17 M14 '
			'M18 M15 '
			'-   -   '
			'N17 P15 '
			'P18 P16 '
			'M19 N15 '
			'M20 N16 '
			'-   -   '
			'N18 -   '
			'P19 R16 '
			'N20 R17 '
			'P20 T20 '
			'-   U20 '
			'-   -   '
			'T16 V20 '
			'U17 W20 '
			'U18 T17 '
			'U19 R18 '
			'-   -   '
			'W18 V17 '
			'W19 V18 '
			'U14 V16 '
			'U15 W16 '
			'-   -   '
			'V15 Y18 '
			'W15 Y19 '
			'Y16 W14 '
			'Y17 Y14 '
			'-   -   '
			'-   -   '
			'-   -   '
			'-   -   '
			'-   -   '
		),
	]
