from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class ListItem(QFrame):
	def __init__(self, name, image_path, show_image_res=True):
		super().__init__()
		self.setFixedSize(80, 140)

		# Create the image label
		self.image_label = QLabel(self)
		pixmap = QPixmap(image_path)

		# resizing is broken
		self.image_label.setPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))

		# Create a vertical layout for text and buttons
		text_layout = QVBoxLayout()
		name_label = QLabel(name)
		name_label.setStyleSheet("font-size: 14px;")
		text_layout.addWidget(self.image_label)
		text_layout.addWidget(name_label)

		if show_image_res:
			size_label = QLabel(f"{pixmap.width()}x{pixmap.height()}")
			size_label.setStyleSheet("font-size: 10px;")
			text_layout.addWidget(size_label)

		# Frame for outline
		self.setFrameShape(QFrame.Box)
		self.setLayout(text_layout)
