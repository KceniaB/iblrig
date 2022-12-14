from confapp import conf



if conf.PYFORMS_MODE in ['GUI']:

    from iblpybpod.pyforms_gui.allcontrols import *

elif conf.PYFORMS_MODE in ['TERMINAL']:

    from iblpybpod.pyforms_terminal.allcontrols import *

elif conf.PYFORMS_MODE in ['WEB']:

    from iblpybpod.pyforms_web.allcontrols import *