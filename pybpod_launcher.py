import os
import pybpod.pybpodgui_plugin.__main__ as pybpod_launcher
from iblrig.path_helper import get_pybpod_working_path

if __name__ == "__main__":
    print("pybpod working path: ", get_pybpod_working_path())
    os.chdir(get_pybpod_working_path())
    print("current dir: ", os.getcwd())
    pybpod_launcher.start()