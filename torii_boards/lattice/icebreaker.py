# SPDX-License-Identifier: BSD-2-Clause

from torii.build                         import (
	Connector, Resource, Pins, Clock, Attrs, PinsN
)
from torii.build.run                     import BuildProducts
from torii.platform.vendor.lattice_ice40 import LatticeICE40Platform
from torii.platform.resources            import (
	LEDResources, ButtonResources, UARTResource, SPIFlashResources
)

__all__ = (
	'ICEBreakerPlatform',
)


class ICEBreakerPlatform(LatticeICE40Platform):
	device      = 'iCE40UP5K'
	package     = 'SG48'
	default_clk = 'clk12'

	resources   = [
		Resource(
			'clk12', 0, Pins('35', dir = 'i'), Clock(12e6),
			Attrs(GLOBAL = True, IO_STANDARD = 'SB_LVCMOS')
		),

		*LEDResources(pins = '11 37', invert = True, attrs = Attrs(IO_STANDARD = 'SB_LVCMOS')),
		# Semantic aliases
		Resource('led_r', 0, PinsN('11', dir = 'o'), Attrs(IO_STANDARD = 'SB_LVCMOS')),
		Resource('led_g', 0, PinsN('37', dir = 'o'), Attrs(IO_STANDARD = 'SB_LVCMOS')),

		*ButtonResources(pins = '10', invert = True, attrs = Attrs(IO_STANDARD = 'SB_LVCMOS')),

		UARTResource(0,
			rx = '6', tx = '9',
			attrs = Attrs(IO_STANDARD = 'SB_LVTTL', PULLUP = 1)
		),

		*SPIFlashResources(0,
			cs_n = '16', clk = '15', copi = '14', cipo = '17', wp_n = '12', hold_n = '13',
			attrs = Attrs(IO_STANDARD = 'SB_LVCMOS')
		),
	]
	connectors = [
		Connector('pmod', 0, ' 4  2 47 45 - -  3 48 46 44 - -'), # PMOD1A
		Connector('pmod', 1, '43 38 34 31 - - 42 36 32 28 - -'), # PMOD1B
		Connector('pmod', 2, '27 25 21 19 - - 26 23 20 18 - -'), # PMOD2
	]
	# The attached LED/button section can be either used standalone or as a PMOD.
	# Attach to platform using:
	# p.add_resources(p.break_off_pmod)
	# pmod_btn = plat.request('user_btn')
	break_off_pmod = [
		*LEDResources(
			pins = {
				2: '7', 3: '1', 4: '2', 5: '8', 6: '3'
			}, conn = ('pmod', 2), attrs = Attrs(IO_STANDARD = 'SB_LVCMOS')
		),
		# Semantic aliases
		Resource(
			'led_r', 1, Pins('7', dir = 'o', conn = ('pmod', 2)), Attrs(IO_STANDARD = 'SB_LVCMOS')
		),
		Resource(
			'led_g', 1, Pins('1', dir = 'o', conn = ('pmod', 2)), Attrs(IO_STANDARD = 'SB_LVCMOS')
		),
		Resource(
			'led_g', 2, Pins('2', dir = 'o', conn = ('pmod', 2)), Attrs(IO_STANDARD = 'SB_LVCMOS')
		),
		Resource(
			'led_g', 3, Pins('8', dir = 'o', conn = ('pmod', 2)), Attrs(IO_STANDARD = 'SB_LVCMOS')
		),
		Resource(
			'led_g', 4, Pins('3', dir = 'o', conn = ('pmod', 2)), Attrs(IO_STANDARD = 'SB_LVCMOS')
		),

		*ButtonResources(
			pins = {
				1: '9', 2: '4', 3: '10'
			}, conn = ('pmod', 2), attrs = Attrs(IO_STANDARD = 'SB_LVCMOS')
		),
	]

	def toolchain_program(self, products: BuildProducts, name: str) -> None:
		from os         import environ
		from subprocess import check_call

		iceprog = environ.get('ICEPROG', 'iceprog')
		with products.extract(f'{name}.bin') as bitstream_filename:
			check_call([iceprog, bitstream_filename])


if __name__ == '__main__':
	from ..test.blinky import Blinky
	p = ICEBreakerPlatform()
	p.add_resources(p.break_off_pmod)
	p.build(Blinky(), do_program = True)
