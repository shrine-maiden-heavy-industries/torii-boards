# SPDX-License-Identifier: BSD-2-Clause

from torii.build                         import Connector, Resource, Pins, Clock, Attrs
from torii.build.run                     import BuildProducts
from torii.platform.vendor.lattice_ice40 import LatticeICE40Platform
from torii.platform.resources            import (
	LEDResources, RGBLEDResource, DirectUSBResource, SPIFlashResources
)

__all__ = (
	'FomuHackerPlatform',
)


class FomuHackerPlatform(LatticeICE40Platform):
	device      = 'iCE40UP5K'
	package     = 'UWG30'
	default_clk = 'clk48'

	resources   = [
		Resource(
			'clk48', 0, Pins('F5', dir = 'i'), Clock(48e6),
			Attrs(GLOBAL = True, IO_STANDARD = 'SB_LVCMOS')
		),

		*LEDResources(pins = 'A5', invert = True, attrs = Attrs(IO_STANDARD = 'SB_LVCMOS')),
		RGBLEDResource(0,
			r = 'C5', g = 'B5', b = 'A5', invert = True,
			attrs = Attrs(IO_STANDARD = 'SB_LVCMOS')
		),

		DirectUSBResource(0, d_p = 'A4', d_n = 'A2', pullup = 'D5',
			attrs = Attrs(IO_STANDARD = 'SB_LVCMOS'),
		),

		*SPIFlashResources(0,
			cs_n = 'C1', clk = 'D1', copi = 'F1', cipo = 'E1',
			attrs = Attrs(IO_STANDARD = 'SB_LVCMOS'),
		),
	]

	connectors = [
		Connector('pin', 0, 'F4'),
		Connector('pin', 1, 'E5'),
		Connector('pin', 2, 'E4'),
		Connector('pin', 3, 'F2'),
	]

	def toolchain_program(self, products: BuildProducts, name: str) -> None:
		from os         import environ
		from subprocess import check_call

		dfu_util = environ.get('DFU_UTIL', 'dfu-util')
		with products.extract(f'{name}.bin') as bitstream_filename:
			check_call([dfu_util, '-D', bitstream_filename])


if __name__ == '__main__':
	from ..test.blinky import Blinky
	FomuHackerPlatform().build(Blinky(), do_program = True)
