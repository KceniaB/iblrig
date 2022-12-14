from confapp import conf

from iblpybpod.pybpodgui_plugin.models.setup.setup_uibusy import SetupUIBusy

Setup = type(
    'Setup',
    tuple(conf.GENERIC_EDITOR_PLUGINS_FINDER.find_class('models.setup.Setup') + [SetupUIBusy]),
    {}
)
