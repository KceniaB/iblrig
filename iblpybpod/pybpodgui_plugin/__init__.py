from confapp import conf

from iblpybpod import loggingbootstrap


conf += "iblpybpod.pybpodgui_plugin.settings"
conf += "iblpybpod.pybpodgui_plugin.resources"

# setup different loggers but output to single file
loggingbootstrap.create_double_logger("pybpodgui_plugin", conf.APP_LOG_HANDLER_CONSOLE_LEVEL,
                                      conf.APP_LOG_FILENAME,
                                      conf.APP_LOG_HANDLER_FILE_LEVEL)

loggingbootstrap.create_double_logger("pybranch", conf.APP_LOG_HANDLER_CONSOLE_LEVEL,
                                      conf.APP_LOG_FILENAME,
                                      conf.APP_LOG_HANDLER_FILE_LEVEL)

loggingbootstrap.create_double_logger("pybpodapi", conf.APP_LOG_HANDLER_CONSOLE_LEVEL,
                                      conf.APP_LOG_FILENAME,
                                      conf.APP_LOG_HANDLER_FILE_LEVEL)

if conf.USE_MULTIPROCESSING:
    # https://docs.python.org/3.5/library/multiprocessing.html#multiprocessing.freeze_support
    from multiprocessing import freeze_support  # @UnresolvedImport
    freeze_support()
