# SPDX-License-Identifier: BSD-2-Clause

from textwrap                      import dedent
from typing                        import TYPE_CHECKING

from torii.build                   import Attrs, Clock, Connector, Pins, Resource
from torii.build.run               import BuildProducts
from torii.hdl.time                import MHz
from torii.platform.resources.user import ButtonResources, LEDResources, SwitchResources
from torii.platform.vendor.altera  import AlteraPlatform

__all__ = (
	'ArrowDECAPlatform',
)

class ArrowDECAPlatform(AlteraPlatform):
	# MAX 10
	device: str  = '10M50DA' # pyright: ignore[reportIncompatibleMethodOverride]
	package: str = 'F484'    # pyright: ignore[reportIncompatibleMethodOverride]
	speed: str   = 'C6'      # pyright: ignore[reportIncompatibleMethodOverride]
	suffix       = 'GES'
	default_clk  = 'clk50'

	pretty_name = 'DECA Development Kit'
	description = 'Arrow Development Tools DECA Altera MAX10 Development Kit'

	resources: list[Resource] = [ # pyright: ignore[reportIncompatibleMethodOverride]
		Resource('clk50', 0, Pins('M8', dir = 'i'), Clock(MHz(50)), Attrs(io_standard = '2.5 V')),
		Resource('clk50', 1, Pins('P11', dir = 'i'), Clock(MHz(50)), Attrs(io_standard = '3.3 V')),
		Resource('clk50', 2, Pins('N15', dir = 'i'), Clock(MHz(50)), Attrs(io_standard = '1.5 V')),
		Resource('clk10', 0, Pins('M9', dir = 'i'), Clock(MHz(10)), Attrs(io_standard = '2.5 V')),
		*LEDResources(
			pins = 'C7 C8 A6 B7 C4 A5 B4 C5',
			invert = True,
			attrs = Attrs(io_standard = '1.2 V')
		),
		*ButtonResources(
			pins = 'H21 H22',
			invert = True,
			attrs = Attrs(io_standard = '1.5 V')
		),
		*SwitchResources(
			pins = 'J21 J22',
			attrs = Attrs(io_standard = '1.5 V')
		),
	]

	connectors: list[Connector] = [
		Connector(
			'gpio', 0,
			'W18  Y18  Y19  AA17 AA20 AA19 AB21 AB20 AB19 Y16  V16  '
			'AB18 V15  W17  AB17 AA16 AB16 W16  AB15 W15  Y14  AA15 '
			'AB14 AA14 AB13 AA13 AB12 AA12 AB11 AA11 AB10 Y13  Y11  '
			'W13  W12  W11  V12  V11  V13  V14  Y17  W14  U15  R13  '
		),
		Connector(
			'gpio', 1,
			'Y5  Y6  W6  W7  W8  V8  AB8 V7  R11 AB7 AB6 '
			'AA7 AA6 Y7  V10 U7  W9  W5  R9  W4  P9  V17 '
			'W3  -   -   -   -   -   -   -   -   -   -   '
		),
	]

	def toolchain_program(self, products: BuildProducts, name: str, **kwargs) -> None:
		from os         import environ
		from subprocess import check_call

		quartus_pgm = environ.get('QUARTUS_PGM', 'quartus_pgm')
		with products.extract(f'{name}.sof') as bitstream_filename:

			if TYPE_CHECKING:
				assert isinstance(bitstream_filename, str)

			check_call([
				quartus_pgm, '--haltcc', '--mode', 'JTAG',
				'--operation', 'P;' + bitstream_filename
			])

	@property
	def file_templates(self) -> dict[str, str]:
		# Configure the voltages of the I/O banks by appending the global
		# assignments to the template. However, we create our own copy of the
		# file templates before modifying them to avoid modifying the original.

		parent_qsf = super().file_templates.get('{{name}}.qsf')

		if TYPE_CHECKING:
			assert isinstance(parent_qsf, str)

		return {
			**super().file_templates,
			'{{name}}.qsf': parent_qsf + dedent(r'''
				set_global_assignment -name IOBANK_VCCIO 2.5V -section_id 1A
				set_global_assignment -name IOBANK_VCCIO 2.5V -section_id 1B
				set_global_assignment -name IOBANK_VCCIO 2.5V -section_id 2
				set_global_assignment -name IOBANK_VCCIO 3.3V -section_id 3
				set_global_assignment -name IOBANK_VCCIO 3.3V -section_id 4
				set_global_assignment -name IOBANK_VCCIO 1.5V -section_id 5
				set_global_assignment -name IOBANK_VCCIO 1.5V -section_id 6
				set_global_assignment -name IOBANK_VCCIO 1.8V -section_id 7
				set_global_assignment -name IOBANK_VCCIO 1.2V -section_id 8

				set_global_assignment -name FORCE_CONFIGURATION_VCCIO ON
				set_global_assignment -name AUTO_RESTART_CONFIGURATION OFF
				set_global_assignment -name ENABLE_CONFIGURATION_PINS OFF
				set_global_assignment -name ENABLE_BOOT_SEL_PIN OFF
			''')
		}


if __name__ == '__main__':
	from ...test.blinky import Blinky
	ArrowDECAPlatform().build(Blinky(), do_program = True)
