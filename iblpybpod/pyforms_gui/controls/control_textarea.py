import iblpybpod.pyforms_gui.utils.tools as tools
from AnyQt 		import uic, QtGui
from iblpybpod.pyforms_gui.controls.control_base import ControlBase

class ControlTextArea(ControlBase):

	def __init__(self, *args, **kwargs):
		ControlBase.__init__(self, *args, **kwargs)
		self.autoscroll = kwargs.get('autoscroll', False)
		
		

	def init_form(self):
		control_path = tools.getFileInSameDirectory(__file__, "textArea.ui")
		self._form = uic.loadUi(control_path)
		self._form.label.setText(self._label)
		if self._value:
			self._form.plainTextEdit.setPlainText(str(self._value))

		if not self._label or len(self._label)==0: 
			self.form.label.hide()

		super(ControlTextArea, self).init_form()
		self.form.plainTextEdit.textChanged.connect(self.finishEditing)

	def __add__(self, other):
		self._form.plainTextEdit.appendPlainText(str(other))

		# if activated the text field is autoscrolled to the bottom
		if self.autoscroll:
			self._form.plainTextEdit.moveCursor(QtGui.QTextCursor.End)

		return self

	def finishEditing(self):
		"""Function called when the lineEdit widget is edited"""
		self.changed_event()
		

	@property
	def value(self):
		return self._form.plainTextEdit.toPlainText()

	@value.setter
	def value(self, value):
		self._form.plainTextEdit.setPlainText(str(value))

	@property
	def readonly(self):
		return self._form.plainTextEdit.isReadOnly()

	@readonly.setter
	def readonly(self, value):
		self._form.plainTextEdit.setReadOnly(value)


	@property
	def autoscroll(self): return self._autoscroll
	@autoscroll.setter
	def autoscroll(self, value): self._autoscroll = value
