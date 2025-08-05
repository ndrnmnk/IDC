from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt


class VariableDelWindow(QWidget):
	def __init__(self, parent, vname, usages):
		super().__init__(parent.wv.parent)

		self.parent = parent
		self.usages = usages

		self.setWindowFlags(Qt.Window)
		self.setWindowTitle("IDC: Delete variable")

		self.vbox = QVBoxLayout()
		self.btn_hbox = QHBoxLayout()

		self.vbox.addWidget(QLabel(f"Variable \"{vname}\" has {usages[0]} usages in {usages[1]} sprites."))
		self.vbox.addWidget(QLabel("Deleting it will remove those references."))
		self.vbox.addWidget(QLabel("Are you sure?"))

		self.btn_cancel = QPushButton("Cancel")
		self.btn_delete = QPushButton("Delete")

		self.btn_hbox.addWidget(self.btn_cancel)
		self.btn_hbox.addWidget(self.btn_delete)

		self.btn_cancel.pressed.connect(self.deleteLater)
		self.btn_delete.pressed.connect(self.delete_var)

		self.vbox.addLayout(self.btn_hbox)

		self.setLayout(self.vbox)
		self.show()

	def delete_var(self):
		self.parent._delete_var_and_ref(self.usages[2], self.usages[3])
		self.deleteLater()