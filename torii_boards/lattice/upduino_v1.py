# SPDX-License-Identifier: BSD-2-Clause

from torii.build                         import Attrs, Connector, PinsN, Resource
from torii.platform.resources            import LEDResources, SPIFlashResources
from torii.platform.vendor.lattice.ice40 import ICE40Platform

__all__ = (
	'UpduinoV1Platform',
)

class UpduinoV1Platform(ICE40Platform):
	device      = 'iCE40UP5K'
	package     = 'SG48'
	default_clk = 'SB_HFOSC'
	hfosc_div   = 0

	pretty_name = 'Upduino V1'
	description = 'TinyVision Upduino V1 Lattice iCE40-UP5K Development Board'

	resources   = [
		*LEDResources(
			pins = '39 40 41', invert = True, attrs = Attrs(IO_STANDARD = 'SB_LVCMOS')
		),
		Resource('led_g', 0, PinsN('39', dir = 'o'), Attrs(IO_STANDARD = 'SB_LVCMOS')),
		Resource('led_b', 0, PinsN('40', dir = 'o'), Attrs(IO_STANDARD = 'SB_LVCMOS')),
		Resource('led_r', 0, PinsN('41', dir = 'o'), Attrs(IO_STANDARD = 'SB_LVCMOS')),

		*SPIFlashResources(0,
			cs_n = '16', clk = '15', cipo = '17', copi = '14',
			attrs = Attrs(IO_STANDARD = 'SB_LVCMOS')
		),
	]
	connectors  = [
		# 'Left' row of header pins (JP5 on the schematic)
		Connector('j', 0, '- - 23 25 26 27 32 35 31 37 34 43 36 42 38 28'),
		# 'Right' row of header pins (JP6 on the schematic)
		Connector('j', 1, '12 21 13 19 18 11 9 6 44 4 3 48 45 47 46 2')
	]

	# This board doesn't have an integrated programmer.
