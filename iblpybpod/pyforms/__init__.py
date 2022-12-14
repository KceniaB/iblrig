from confapp import conf

conf += "iblpybpod.pyforms.settings"

try:
    import local_settings
    conf += local_settings
except:
    pass


if conf.PYFORMS_MODE == 'GUI':

    from iblpybpod.pyforms_gui.appmanager import start_app

elif conf.PYFORMS_MODE == 'TERMINAL':

    from iblpybpod.pyforms_terminal.appmanager import start_app