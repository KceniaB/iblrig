from confapp import conf
from iblpybpod.pybpodgui_plugin.models.experiment.experiment_uibusy import ExperimentUIBusy

Experiment = type(
    'Experiment',
    tuple(conf.GENERIC_EDITOR_PLUGINS_FINDER.find_class('models.experiment.Experiment') + [ExperimentUIBusy]),
    {}
)
