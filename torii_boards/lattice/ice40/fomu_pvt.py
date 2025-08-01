# SPDX-License-Identifier: BSD-2-Clause

from torii.build                         import Attrs, Clock, Pins, Resource
from torii.build.run                     import BuildProducts
from torii.platform.resources            import DirectUSBResource, LEDResources, RGBLEDResource, SPIFlashResources
from torii.platform.vendor.lattice.ice40 import ICE40Platform

__all__ = (
	'FomuPVTPlatform',
)

class FomuPVTPlatform(ICE40Platform):
	device      = 'iCE40UP5K'
	package     = 'UWG30'
	default_clk = 'clk48'

	pretty_name = 'FOMU'
	description = 'Im Tomu FPGA Lattice iCE40 UP5K FPGA Board'

	resources   = [
		Resource(
			'clk48', 0, Pins('F4', dir = 'i'), Clock(48e6),
			Attrs(GLOBAL = True, IO_STANDARD = 'SB_LVCMOS')
		),

		*LEDResources(pins = 'A5', invert = True, attrs = Attrs(IO_STANDARD = 'SB_LVCMOS')),
		RGBLEDResource(0,
			r = 'B5', g = 'A5', b = 'C5', invert = True,
			attrs = Attrs(IO_STANDARD = 'SB_LVCMOS')
		),


		DirectUSBResource(0,
			d_p = 'A1', d_n = 'A2', pullup = 'A4',
			attrs = Attrs(IO_STANDARD = 'SB_LVCMOS')
		),

		*SPIFlashResources(0,
			cs_n = 'C1', clk = 'D1', copi = 'F1', cipo = 'E1',
			attrs = Attrs(IO_STANDARD = 'SB_LVCMOS'),
		),

		Resource('touch', 0, Pins('E4')),
		Resource('touch', 1, Pins('D5')),
		Resource('touch', 2, Pins('E5')),
		Resource('touch', 3, Pins('F5')),
	]

	def toolchain_program(self, products: BuildProducts, name: str) -> None:
		from os         import environ
		from subprocess import check_call

		dfu_util = environ.get('DFU_UTIL', 'dfu-util')
		with products.extract(f'{name}.bin') as bitstream_filename:
			check_call([dfu_util, '-D', bitstream_filename])


if __name__ == '__main__':
	from ...test.blinky import Blinky
	FomuPVTPlatform().build(Blinky(), do_program = True)
