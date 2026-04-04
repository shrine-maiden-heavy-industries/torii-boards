# SPDX-License-Identifier: BSD-2-Clause

from torii.build                   import Attrs, Clock, Connector, DiffPairs, Resource
from torii.build.run               import BuildProducts
from torii.hdl.time                import MHz
from torii.platform.resources.user import LEDResources
from torii.platform.vendor.xilinx  import XilinxPlatform

__all__ = (
	'KCU105Platform',
)

class KCU105Platform(XilinxPlatform):
	device: str  = 'xcku040'  # pyright: ignore[reportIncompatibleMethodOverride]
	package: str = 'ffva1156' # pyright: ignore[reportIncompatibleMethodOverride]
	speed: str   = '2-e'      # pyright: ignore[reportIncompatibleMethodOverride]
	default_clk  = 'clk125'

	pretty_name = 'KCU105'
	description = 'Xilinx Kintex UltraScale Evaluation Board'

	resources: list[Resource] = [ # pyright: ignore[reportIncompatibleMethodOverride]
		Resource(
			'clk125', 0, DiffPairs('G10', 'F10', dir = 'i'), Clock(MHz(125)), Attrs(IOSTANDARD = 'LVDS')
		),
		*LEDResources(
			pins = 'AP8 H23 P20 P21 N22 M22 R23 P23',
			attrs = Attrs(IOSTANDARD = 'LVCMOS18')
		),
	]

	connectors: list[Connector] = []

	def toolchain_program(self, products: BuildProducts, name: str, **kwargs) -> None:
		from os         import environ
		from subprocess import check_call

		openocd = environ.get('OPENOCD', 'openocd')
		with products.extract(f'{name}.bit') as bitstream_filename:
			check_call([
				openocd, '-c', f'source [find board/kcu105.cfg]; init; pld load 0 {bitstream_filename}; exit'
			])


if __name__ == '__main__':
	from ...test.blinky import Blinky
	KCU105Platform().build(Blinky(), do_program = True)
