from confapp import conf


if conf.PYFORMS_MODE in ['GUI']:

    from iblpybpod.pyforms_gui.basewidget import BaseWidget
    from iblpybpod.pyforms_gui.organizers import vsplitter, hsplitter, segment, no_columns

elif conf.PYFORMS_MODE in ['TERMINAL']:

    from iblpybpod.pyforms_terminal.basewidget import BaseWidget
    no_columns = tuple
    segment = list
    
elif conf.PYFORMS_MODE in ['WEB']:

    from iblpybpod.pyforms_web.basewidget import BaseWidget
    from iblpybpod.pyforms_web.organizers import no_columns, segment
    
    from iblpybpod.pyforms_web.modeladmin import ModelAdmin
    from iblpybpod.pyforms_web.modeladmin import ViewFormAdmin
    from iblpybpod.pyforms_web.modeladmin import EditFormAdmin
