# SPDX-License-Identifier: BSD-2-Clause

from torii.build                  import Attrs, Clock, Connector, Pins, Resource
from torii.build.run              import BuildProducts
from torii.platform.resources     import (
	ButtonResources, Display7SegResource, LEDResources, PS2Resource, SDCardResources, SDRAMResource,
	SwitchResources, VGAResource
)
from torii.platform.vendor.altera import AlteraPlatform

__all__ = (
	'DE0CVPlatform',
)

class DE0CVPlatform(AlteraPlatform):
	device      = '5CEBA4' # Cyclone V 49K LEs
	package     = 'F23'    # FBGA-484
	speed       = 'C7'
	default_clk = 'clk50'

	pretty_name = 'DE0-CV'
	description = 'terasIC DE0-CV Altera Cyclone V Development Board'

	resources   = [
		Resource(
			'clk50', 0, Pins('M9', dir = 'i'),  Clock(50e6), Attrs(io_standard = '3.3-V LVTTL')
		),
		Resource(
			'clk50', 1, Pins('H13', dir = 'i'), Clock(50e6), Attrs(io_standard = '3.3-V LVTTL')
		),
		Resource(
			'clk50', 2, Pins('E10', dir = 'i'), Clock(50e6), Attrs(io_standard = '3.3-V LVTTL')
		),
		Resource(
			'clk50', 3, Pins('V15', dir = 'i'), Clock(50e6), Attrs(io_standard = '3.3-V LVTTL')
		),

		*LEDResources(
			pins = 'AA2 AA1 W2 Y3 N2 N1 U2 U1 L2 L1', invert = True,
			attrs = Attrs(io_standard = '3.3-V LVTTL')
		),
		*ButtonResources(
			pins = 'U7 W9 M7 M6', invert = True,
			attrs = Attrs(io_standard = '3.3-V LVTTL')
		),
		*SwitchResources(
			pins = 'U13 V13 T13 T12 AA15 AB15 AA14 AA13 AB13 AB12',
			attrs = Attrs(io_standard = '3.3-V LVTTL')
		),
		Display7SegResource(0,
			a = 'U21', b = 'V21', c = 'W22', d = 'W21', e = 'Y22', f = 'Y21', g = 'AA22', invert = True,
			attrs = Attrs(io_standard = '3.3-V LVTTL')
		),
		Display7SegResource(1,
			a = 'AA20', b = 'AB20', c = 'AA19', d = 'AA18', e = 'AB18', f = 'AA17', g = 'U22', invert = True,
			attrs = Attrs(io_standard = '3.3-V LVTTL')),
		Display7SegResource(2,
			a = 'Y19', b = 'AB17', c = 'AA10', d = 'Y14', e = 'V14', f = 'AB22', g = 'AB21', invert = True,
			attrs = Attrs(io_standard = '3.3-V LVTTL')
		),
		Display7SegResource(3,
			a = 'Y16', b = 'W16', c = 'Y17', d = 'V16', e = 'U17', f = 'V18', g = 'V19', invert = True,
			attrs = Attrs(io_standard = '3.3-V LVTTL')
		),
		Display7SegResource(4,
			a = 'U20', b = 'Y20', c = 'V20', d = 'U16', e = 'U15', f = 'Y15', g = 'P9', invert = True,
			attrs = Attrs(io_standard = '3.3-V LVTTL')
		),
		Display7SegResource(5,
			a = 'N9', b = 'M8', c = 'T14', d = 'P14', e = 'C1', f = 'C2', g = 'W19', invert = True,
			attrs = Attrs(io_standard = '3.3-V LVTTL')
		),

		VGAResource(0,
			r = 'A9 B10 C9 A5',
			g = 'L7 K7 J7 J8',
			b = 'B6 B7 A8 A7',
			hs = 'H8', vs = 'G8',
			attrs = Attrs(io_standard = '3.3-V LVTTL')
		),

		PS2Resource(0, # Keyboard
			clk = 'D3', dat = 'G2', attrs = Attrs(io_standard = '3.3-V LVTTL')
		),
		PS2Resource(1, # Mouse
			clk = 'E2', dat = 'G1', attrs = Attrs(io_standard = '3.3-V LVTTL')
		),

		*SDCardResources(0,
			clk = 'H11', cmd = 'B11', dat0 = 'K9', dat1 = 'D12', dat2 = 'E12', dat3 = 'C11',
			attrs = Attrs(io_standard = '3.3-V LVTTL')
		),

		SDRAMResource(0,
			clk = 'AB11', cke = 'R6', cs_n = 'U6', we_n = 'AB5', ras_n = 'AB6', cas_n = 'V6',
			ba = 'T7 AB7', a = 'W8 T8 U11 Y10 N6 AB10 P12 P7 P8 R5 U8 P6 R7',
			dq = 'Y9 T10 R9 Y11 R10 R11 R12 AA12 AA9 AB8 AA8 AA7 V10 V9 U10 T9', dqm = 'U12 N8',
			attrs = Attrs(io_standard = '3.3-V LVCMOS')
		),
	]
	connectors  = [
		Connector('j', 1,
			'N16  B16  M16  C16  D17  K20  K21  K22  M20  M21  '
			'-    -    N21  R22  R21  T22  N20  N19  M22  P19  '
			'L22  P17  P16  M18  L18  L17  L19  K17  -    -    '
			'K19  P18  R15  R17  R16  T20  T19  T18  T17  T15  '
		),
		Connector('j', 2,
			'H16  A12  H15  B12  A13  B13  C13  D13  G18  G17  '
			'-    -    H18  J18  J19  G11  H10  J11  H14  A15  '
			'J13  L8   A14  B15  C15  E14  E15  E16  -    -    '
			'F14  F15  F13  F12  G16  G15  G13  G12  J17  K16  '
		),
	]

	def toolchain_program(self, products: BuildProducts, name: str) -> None:
		from os         import environ
		from subprocess import check_call

		quartus_pgm = environ.get('QUARTUS_PGM', 'quartus_pgm')
		with products.extract(f'{name}.sof') as bitstream_filename:
			check_call([
				quartus_pgm, '--haltcc', '--mode', 'JTAG',
				'--operation', 'P;' + bitstream_filename
			])


if __name__ == '__main__':
	from ...test.blinky import Blinky
	DE0CVPlatform().build(Blinky(), do_program = True)
