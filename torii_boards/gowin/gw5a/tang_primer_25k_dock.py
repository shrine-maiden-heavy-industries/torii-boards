# SPDX-License-Identifier: BSD-2-Clause

import subprocess
from enum import Enum, auto
from torii.build import Attrs, Clock, Pins, Resource, Connector
from torii.platform.resources.interface import UARTResource, DirectUSBResource
from torii.platform.resources.memory import SPIFlashResources
from torii.platform.resources.user import ButtonResources, LEDResources
from torii.platform.vendor.gowin import GowinPlatform

__all__ = ("TangPrimer25kDockPlatform",)

class GowinProgrammerOp(Enum):
	"""
	Enumeration of relevant operations for the Gowin programmer_cli tool
	"""

	SRAMProgram = 2
	ExFlashEraseProgram5A = 53
	ExFlashEraseProgramVerify5A = 54


class TangPrimer25kDockPlatform(GowinPlatform):
	"""
	Referenced:
	* https://cdn.gowinsemi.com.cn/DS1103E.pdf
	* https://github.com/YosysHQ/apicula/blob/master/apycula/chipdb.py
	* https://github.com/YosysHQ/apicula/blob/master/examples/gw5a/primer25k.cst
	"""

	part = "GW5A-LV25MG121NC1/I0"
	family = "GW5A-25A"
	default_clk = "clk50m"
	osc_frequency = 50e6

	pretty_name = "Tang Primer 25K Dock"
	description = "Sipeed Tang Primer 25K Dock Gowin GW5A Development Board"

	resources = [
		# External crystal @ 50MHz on pin E2
		Resource(
			"clk50m",
			0,
			Pins("E2", dir="i"),
			Clock(50e6),
			Attrs(IO_TYPE="LVCMOS33", PULL_MODE="NONE", DRIVE="OFF",
				  BANK_VCCIO="3.3"),
		),
		*ButtonResources("button", 0, pins="H10 H11 F5 G7 H7 J5"),
		*LEDResources(
			"led",
			pins="G5", # G8 H7 J5 F5 G7 H8 H5",
			attrs=Attrs(IO_TYPE="LVCMOS33", PULL_MODE="NONE"),
		),
		DirectUSBResource(
			"usb",
			0,
			d_p="L6",
			d_n="K6",
			attrs=Attrs(
				IO_TYPE="LVCMOS33", PULL_MODE="DOWN", DRIVE=8, BANK_VCCIO="3.3"
			),
		),
		UARTResource(0, tx="C3", rx="B3", attrs=Attrs(IO_TYPE="LVCMOS33")),
		# *SPIFlashResources(
		# 	0,
		# 	cs_n="B1",
		# 	clk="C1",
		# 	copi="D6",
		# 	cipo="E5",
		# 	wp_n="E2",
		# 	hold_n="D1",
		# 	attrs=Attrs(IO_TYPE="LVCMOS33"),
		# ),
	]

	connectors = [
		Connector(
			"pmod", 0, "G11 D11 B11 C11 -   -   G10 D10 B10 C10 -   -   "
		),  # PMOD1A
		Connector(
			"pmod", 1, "A11 E11 K11 L5  -   -   A10 E10 L11 K5  -   -   "
		),  # PMOD1B
		Connector(
			"pmod", 2, "F5  G7  H8  H5  -   -   G5  G8  H7  J5  -   -   "
		),  # PMOD2
		Connector(
			"gpio",
			0,
			"K2  K1  L1  L2  K4  J4  G1  G2  L3  L4 "  # 1  - 10
			"-   -   C2  B2  F1  F2  A1  E1  D1  E3 "  # 11 - 20
			"J2  J1  H4  G4  H2  H1  J7  K7  L8  L7 "  # 21 - 30
			"K10 L10 K9  L9  K8  J8  F6  F7  J10 J11",  # 31 - 40
		),
	]

	def __init__(self, *args, toolchain='Gowin', use_gowin_programmer=True,
			gowin_programmer_op=GowinProgrammerOp.SRAMProgram):
		"""
		Tang Primer 25k Dock Platform

		Supports specification of toolchain (only 'Gowin' supported at
		this time) and use_gowin_programmer=True enables use of the
		vendor-supplied programmer_cli tool which can erase and write to
		the embedded flash if specified as the gowin_programmer_op
		operation.

		Warning: writing to exFlash is quite slow via this method.
		
		The gowin programmer options are ignored if 'Apicula'
		toolchain is selected.
		"""
		self.use_gowin_programmer = use_gowin_programmer
		self.gowin_programmer_op = gowin_programmer_op

		super().__init__(*args, toolchain=toolchain)

	def toolchain_prepare(self, fragment, name, **kwargs):
		overrides = {
			"add_options": "set_option -use_sspi_as_gpio 1 -use_cpu_as_gpio 1",
			"gowin_pack_opts": "--sspi_as_gpio --cpu_as_gpio",
		}
		return super().toolchain_prepare(fragment, name, **overrides, **kwargs)

	def toolchain_program(self, products, name):
		with products.extract(f"{name}.fs") as bitstream_filename:
			if self.use_gowin_programmer:
				subprocess.check_call(
					["programmer_cli", "--device", self.family, 
	  				"--frequency", "15MHz", "--operation_index",
	  				f"{self.gowin_programmer_op.value}", "--fsFile", bitstream_filename]
				)
			else:
				# Loads only to SRAM at present, so does not persist upon reset
				subprocess.check_call(
					["openFPGALoader", "-b", "tangprimer25k", bitstream_filename]
				)


if __name__ == "__main__":
	from ...test.blinky import Blinky

	TangPrimer25kDockPlatform().build(Blinky(), do_program=True)
