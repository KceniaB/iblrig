__version__ = '0.1.5'

from iblpybpod.pybpod_gui_plugin_emulator.emulator_gui import EmulatorGUI

from confapp import conf

conf += "iblpybpod.pybpod_gui_plugin_emulator.settings"
conf += "iblpybpod.pybpod_gui_plugin_emulator.resources"
