""" pyforms_gui.controls.ControlLabel """

import iblpybpod.pyforms_gui.utils.tools as tools
from confapp import conf

from AnyQt import uic, QtCore, QtGui

from iblpybpod.pyforms_gui.controls.control_base import ControlBase


class ControlLabel(ControlBase):

    def init_form(self):
        control_path = tools.getFileInSameDirectory(__file__, "label.ui")
        self._form = uic.loadUi(control_path)
        self._form.label.setText(self._label)
        self._selectable = False
        super(ControlLabel, self).init_form()

    def load_form(self, data, path=None): pass

    def save_form(self, data, path=None): pass

    @property
    def selectable(self): return self._selectable

    @selectable.setter
    def selectable(self, value):
        if value:
            self._form.label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
            self._form.label.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        else:
            self._form.label.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
            self._form.label.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    @property
    def form(self): return self._form


    @property
    def value(self): return ControlBase.value.fget(self)

    @value.setter
    def value(self, value):
        self._form.label.setText(value)
        ControlBase.value.fset(self, value)

