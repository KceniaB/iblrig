from confapp import conf
from iblpybpod.pybpodgui_plugin.models.subject.subject_uibusy import SubjectUIBusy

Subject = type(
    'Subject',
    tuple(conf.GENERIC_EDITOR_PLUGINS_FINDER.find_class('models.subject.Subject') + [SubjectUIBusy]),
    {}
)
