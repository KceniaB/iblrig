from confapp import conf

from iblpybpod.pybpodgui_plugin.models.task.task_dockwindow import TaskDockWindow

Task = type(
    'Task',
    tuple(conf.GENERIC_EDITOR_PLUGINS_FINDER.find_class('models.task.Task') + [TaskDockWindow]),
    {}
)
