# SPDX-License-Identifier: BSD-2-Clause

from torii.build                         import Attrs, Clock, Connector, Pins, Resource
from torii.build.run                     import BuildProducts
from torii.hdl.time                      import MHz
from torii.platform.resources.interface  import DirectUSBResource
from torii.platform.resources.memory     import SPIFlashResources
from torii.platform.resources.user       import LEDResources, RGBLEDResource
from torii.platform.vendor.lattice.ice40 import ICE40Platform

__all__ = (
	'FomuHackerPlatform',
)

class FomuHackerPlatform(ICE40Platform):
	device: str  = 'iCE40UP5K' # pyright: ignore[reportIncompatibleMethodOverride]
	package: str = 'UWG30'     # pyright: ignore[reportIncompatibleMethodOverride]
	default_clk  = 'clk48'

	pretty_name = 'FOMU Hacker'
	description = 'Im Tomu FPGA Hacker Edition Lattice iCE40 UP5K FPGA Board'

	resources: list[Resource] = [ # pyright: ignore[reportIncompatibleMethodOverride]
		Resource(
			'clk48', 0,
			Pins('F5', dir = 'i'), Clock(MHz(48)),
			Attrs(GLOBAL = True, IO_STANDARD = 'SB_LVCMOS')
		),
		*LEDResources(pins = 'A5', invert = True, attrs = Attrs(IO_STANDARD = 'SB_LVCMOS')),
		RGBLEDResource(
			0,
			r = 'C5', g = 'B5', b = 'A5', invert = True,
			attrs = Attrs(IO_STANDARD = 'SB_LVCMOS')
		),
		DirectUSBResource(
			0,
			d_p = 'A4', d_n = 'A2', pullup = 'D5',
			attrs = Attrs(IO_STANDARD = 'SB_LVCMOS'),
		),
		*SPIFlashResources(
			0,
			cs_n = 'C1', clk = 'D1', copi = 'F1', cipo = 'E1',
			attrs = Attrs(IO_STANDARD = 'SB_LVCMOS'),
		),
	]

	connectors: list[Connector] = [
		Connector('pin', 0, 'F4'),
		Connector('pin', 1, 'E5'),
		Connector('pin', 2, 'E4'),
		Connector('pin', 3, 'F2'),
	]

	def toolchain_program(self, products: BuildProducts, name: str, **kwargs) -> None:
		from os         import environ
		from subprocess import check_call
		from typing     import TYPE_CHECKING

		dfu_util = environ.get('DFU_UTIL', 'dfu-util')
		with products.extract(f'{name}.bin') as bitstream_filename:

			if TYPE_CHECKING:
				assert isinstance(bitstream_filename, str)

			check_call([dfu_util, '-D', bitstream_filename])


if __name__ == '__main__':
	from ...test.blinky import Blinky
	FomuHackerPlatform().build(Blinky(), do_program = True)
