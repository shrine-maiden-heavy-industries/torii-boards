# SPDX-License-Identifier: BSD-2-Clause

from torii.build                        import Attrs, Clock, Pins, Resource
from torii.build.run                    import BuildProducts
from torii.hdl.time                     import MHz
from torii.platform.resources.interface import UARTResource
from torii.platform.resources.user      import LEDResources
from torii.platform.vendor.xilinx       import XilinxPlatform

__all__ = (
	'EBAZ4205Platform',
)

class EBAZ4205Platform(XilinxPlatform):
	device: str  = 'xc7z010' # pyright: ignore[reportIncompatibleMethodOverride]
	package: str = 'clg400'  # pyright: ignore[reportIncompatibleMethodOverride]
	speed: str   = '1'       # pyright: ignore[reportIncompatibleMethodOverride]
	default_clk  = 'clk33_333'

	pretty_name = 'EBAZ4205'
	description = 'EBAZ4205 Ebit E9+ Xilinx Zynq-7010 Board'

	resources: list[Resource] = [ # pyright: ignore[reportIncompatibleMethodOverride]
		Resource(
			'clk33_333', 0, Pins('N18', dir = 'i'), Clock(MHz(33.333)), Attrs(IOSTANDARD = 'LVCMOS33')
		),
		*LEDResources(
			pins = 'W14 W13',
			attrs = Attrs(IOSTANDARD = 'LVCMOS33')
		),
		UARTResource(
			0,
			rx = 'B19', tx = 'B20',
			attrs = Attrs(IOSTANDARD = 'LVCMOS33')
		),
	]

	connectors = []

	def toolchain_program(self, products: BuildProducts, name: str, **kwargs) -> None:
		from os         import environ
		from subprocess import run
		from typing     import TYPE_CHECKING

		xc3sprog = environ.get('XC3SPROG', 'xc3sprog')
		with products.extract(f'{name}.bit') as bitstream_filename:

			if TYPE_CHECKING:
				assert isinstance(bitstream_filename, str)

			run([xc3sprog, '-c', 'jtaghs1_fast', '-p', '1', bitstream_filename], check = True)


if __name__ == '__main__':
	from ...test.blinky import Blinky
	EBAZ4205Platform().build(Blinky(), do_program = True)
