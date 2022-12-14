from confapp import conf

from iblpybpod.pybpodgui_plugin.models.setup.board_task.board_task_uibusy import BoardTaskUIBusy

BoardTask = type(
    'BoardTask',
    tuple(conf.GENERIC_EDITOR_PLUGINS_FINDER.find_class('models.setup.board_task.BoardTask') + [BoardTaskUIBusy]),
    {}
)
