from confapp import conf
import iblpybpod.loggingbootstrap as loggingbootstrap

# load the user settings
try:
    import user_settings

    conf += user_settings
except:
    pass

conf += "iblpybpod.pybpodapi.settings"

if conf.PYBPOD_API_LOG_LEVEL is not None:
    # setup different loggers for example script and api
    loggingbootstrap.create_double_logger(
        "pybpodapi",
        conf.PYBPOD_API_LOG_LEVEL,
        conf.PYBPOD_API_LOG_FILE,
        conf.PYBPOD_API_LOG_LEVEL,
    )
