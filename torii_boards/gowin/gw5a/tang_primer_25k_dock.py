# SPDX-License-Identifier: BSD-2-Clause

import subprocess

from enum                               import Enum
from torii.build                        import Attrs, Clock, Connector, Pins, Resource
from torii.platform.resources.interface import DirectUSBResource, UARTResource
from torii.platform.resources.memory    import SPIFlashResources
from torii.platform.resources.user      import ButtonResources, LEDResources
from torii.platform.vendor.gowin        import GowinPlatform


__all__ = (
	'TangPrimer25kDockPlatform',
)

class TangPrimer25kDockPlatform(GowinPlatform):
	'''
	Board support for the Sipeed Tang Primer 25K Dock, described here:
	https://wiki.sipeed.com/hardware/en/tang/tang-primer-25k/primer-25k.html

	Referenced:
	* https://cdn.gowinsemi.com.cn/DS1103E.pdf
	* https://github.com/YosysHQ/apicula/blob/master/apycula/chipdb.py
	* https://github.com/YosysHQ/apicula/blob/master/examples/gw5a/primer25k.cst
	'''

	@property
	def part(self):
		'''
		Selects the correct board identifier depending on the selected toolchain.

		The C1/I0 timing detail on the GW5A-LV25MG121N is not being interpreted
		correctly in Apicula but works fine in the Gowin toolchain. Using the 'ES'
		(Engineering Sample) variant of the board in place of 'C1/I0' for the time
		being (as advised by xiwang in the #yosys-apicula IRC channel) appears to
		work fine, but not in the Gowin toolchain.

		Having the part value be dynamic enables either toolchain to be used
		seamlessly while awaiting full support for the C1/I0 configuration in
		Apicula.
		'''

		return 'GW5A-LV25MG121NES' if self.toolchain == 'Apicula' else 'GW5A-LV25MG121NC1/I0'

	family = 'GW5A-25A'

	# This is the 50 MHz crystal on the Primer 25K Dock.
	# The builtin oscillator may also be used by specifying 'OSC'
	# along with a frequency in line with allowed clock divisions:
	# '3 or an even number between 2 and 126.'
	default_clk = 'clk50'
	osc_frequency = 50_000_000

	pretty_name = 'Tang Primer 25K Dock'
	description = 'Sipeed Tang Primer 25K Dock Gowin GW5A Development Board'

	resources = [
			# 50 MHz crystal on the Dock
			Resource(
				'clk50',
				0,
				Pins('E2', dir = 'i'),
				Clock(50_000_000),
				Attrs(IO_TYPE = 'LVCMOS33')
			),

			# Buttons as detailed on the Primer 25k Dock Schematic:
			# https://dl.sipeed.com/shareURL/TANG/Primer_25K/02_Schematic
			*ButtonResources(
				'button',
				pins  = 'H11 H10', # H11 = S1, H10 = S2
				attrs = Attrs(
					IO_TYPE = 'LVCMOS33',
					PULL_MODE = 'DOWN'
				)
			),

			# Builtin LEDs on the Dock. D7 ('Done') has been removed for
			# now as it fails to map under Apicula.
			*LEDResources(
				'led',
				pins  = 'E8', # E8 = 'Ready'
				attrs = Attrs(IO_TYPE = 'LVCMOS33')
			),

			# USB Host Port
			DirectUSBResource(
				'usb',
				0,
				d_p   = 'L6',
				d_n   = 'K6',
				attrs = Attrs(IO_TYPE = 'LVCMOS33')
			),

			# USB Debugger UART on the Dock
			UARTResource(0, tx = 'C3', rx = 'B3', attrs = Attrs(IO_TYPE = 'LVCMOS33')),

			# SPI Flash on the Tang Primer 25K module itself
			*SPIFlashResources(
				0,
				cs_n   = 'B1',
				clk    = 'C1',
				copi   = 'D6',
				cipo   = 'E5',
				wp_n   = 'E2',
				hold_n = 'D1',
				attrs  = Attrs(IO_TYPE = 'LVCMOS33'),
			),
		]

	connectors = [
			# These do not match the pin numbering in the Gowin schematic
			# but do align with the pin numbering on the Type 1A PMOD standard:
			Connector('pmod', 0, 'G11 D11 B11 C11 -   -   G10 D10 B10 C10 -   -'), # J4
			Connector('pmod', 1, 'A11 E11 K11 L5  -   -   A10 E10 L11 K5  -   -'), # J5
			Connector('pmod', 2, 'F5  G7  H8  H5  -   -   G5  G8  H7  J5  -   -'), # J6

			# The remaining exposed GPIO is on a 2x20 pin header and does
			# follow the numbering in the Gowin schematic:
			Connector(
				'gpio',
				0,
				'K2  K1  L1  L2  K4  J4  G1  G2  L3  L4 '  # 1  - 10
				'-   -   C2  B2  F1  F2  A1  E1  D1  E3 '  # 11 - 20
				'J2  J1  H4  G4  H2  H1  J7  K7  L8  L7 '  # 21 - 30
				'K10 L10 K9  L9  K8  J8  F6  F7  J10 J11'  # 31 - 40
			),
		]

	class GowinProgrammerOp(Enum):
		'''
		Enumeration of relevant operations for the Gowin programmer_cli tool
		'''

		SRAMProgram                 = 2
		ExFlashEraseProgram5A       = 53
		ExFlashEraseProgramVerify5A = 54

	_valid_programmers        = ['openFPGALoader', 'programmer_cli']
	_valid_programmer_targets = ['SRAM', 'flash']

	def __init__(
		self,
		*args,
		toolchain: str                = 'Apicula',
		programmer: str               = 'openFPGALoader',
		programmer_target: str        = 'SRAM',
		programmer_verify_flash: bool = True,
		**kwargs,
	):
		'''
		The `toolchain` argument can be either 'Apicula' or 'Gowin' depending on which toolchain
		you have installed and available on the path.

		The `programmer` can be specified as either `openFPGALoader` or `programmer_cli`. The
		tool must be available in the path. The default is to use `openFPGALoader`.

		Your `programmer_target` can be specified as either 'SRAM' or 'flash'. The default is 'SRAM'.

		Default behaviour when writing to flash is to verify, but `programmer_verify_flash` can be set
		to `False` to disable verification.
		'''

		if programmer not in self._valid_programmers:
			raise ValueError(
				f'Specified programmer tool, \'{programmer}\', is not supported. Tool must be one of: '
				'\'openFPGALoader\' or \'programmer_cli\'.'
			)
		self._programmer = programmer

		if programmer_target not in self._valid_programmer_targets:
			raise ValueError(
				f'Programmer target, \'{programmer_target}\', is not supported. Please specify one of: '
				'\'SRAM\' or \'ExFlash\'.'
			)
		self._programmer_target       = programmer_target
		self._programmer_verify_flash = programmer_verify_flash

		super().__init__(*args, toolchain = toolchain, **kwargs)

	def toolchain_prepare(self, fragment, name, **kwargs):
		options = {
			'ready_as_gpio': 1,
			'done_as_gpio':  1,
			'mspi_as_gpio':  1,
			'sspi_as_gpio':  1,
			'cpu_as_gpio':   1
		}
		add_options        = ' '.join([f'-use_{k} {v}' for k, v in options.items()])
		nextpnr_options    = ' '.join([f'--vopt {k}={v}' for k, v in options.items()])
		gowin_pack_options = ' '.join([f'--{k}' for k, v in options.items() if v == 1])

		return super().toolchain_prepare(
			fragment,
			name,
			add_options     = f'set_option {add_options}',
			nextpnr_opts    = nextpnr_options,
			gowin_pack_opts = gowin_pack_options,
			**kwargs
		)

	def toolchain_program(self, products, name, **kwargs):
		with products.extract(f'{name}.fs') as bitstream_filename:
			if self._programmer == 'programmer_cli':
				if self._programmer_target == 'flash':
					if self._programmer_verify_flash:
						programmer_op = self.GowinProgrammerOp.ExFlashEraseProgramVerify5A
					else:
						programmer_op = self.GowinProgrammerOp.ExFlashEraseProgram5A
				else:
					programmer_op = self.GowinProgrammerOp.SRAMProgram

				subprocess.check_call(
					[
						'programmer_cli',
						'--device',
						self.family,
						'--frequency',
						'15MHz',
						'--operation_index',
						f'{programmer_op.value}',
						'--fsFile',
						str(bitstream_filename),
					]
				)
			else:
				program_command = ['openFPGALoader']

				if self._programmer_target == 'flash':
					program_command.append('-f')
					if self._programmer_verify_flash:
						program_command.append('--verify')
				else:
					program_command.append('-m')

				program_command.extend(['-b', 'tangprimer25k', str(bitstream_filename)])
				subprocess.check_call(program_command)


if __name__ == '__main__':
	from ...test.blinky import Blinky

	TangPrimer25kDockPlatform().build(Blinky(), do_program = True)
