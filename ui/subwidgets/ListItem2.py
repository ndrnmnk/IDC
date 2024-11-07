from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from io import BytesIO
import requests


class ImageDownloader(QThread):
	image_downloaded = pyqtSignal(QPixmap)

	def __init__(self, url):
		super().__init__()
		self.url = url

	def run(self):
		try:
			response = requests.get(self.url)
			response.raise_for_status()
			image_data = BytesIO(response.content)
			pixmap = QPixmap()
			pixmap.loadFromData(image_data.read())
			self.image_downloaded.emit(pixmap)
		except Exception as e:
			print(f"Error downloading image: {e}")


class ListItem(QWidget):
	def __init__(self, manager, name, description, img_url=None, git_link=None):
		super().__init__()

		self.manager = manager
		self.git_link = git_link
		self.name = name

		hbox = QHBoxLayout()
		vbox = QVBoxLayout()
		buttons_hbox = QHBoxLayout()
		hbox.setAlignment(Qt.AlignLeft)
		vbox.setAlignment(Qt.AlignTop)
		buttons_hbox.setAlignment(Qt.AlignLeft)

		self.image_label = QLabel()
		# Set a placeholder image initially from disk
		placeholder_pixmap = QPixmap("textures/logo.png")
		self.image_label.setPixmap(placeholder_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
		if img_url:
			self.download_image_from_url(img_url)

		self.btn = QPushButton()
		self.btn.setFixedWidth(64)
		if self.git_link is None or name in self.manager.ia:
			self.btn.setText("Uninstall")
			self.btn.pressed.connect(self.uninstall_module)
			if name in self.manager.to_update:
				print(name + " could be updated")
				self.btn2 = QPushButton()
				self.btn2.setText("Update")
				self.btn2.pressed.connect(lambda: self.manager.update_addon(self))
				buttons_hbox.addWidget(self.btn2)
		else:
			self.btn.setText("Install")
			self.btn.pressed.connect(self.install_module)

		if self.git_link is None:
			title_label = QLabel(self.name)
		else:
			title_label = QLabel(f"<a href='{git_link}'>{name}</a>")
		title_label.setOpenExternalLinks(True)
		title_label.setStyleSheet("font-size: 14pt;")

		hbox.addWidget(self.image_label)
		hbox.addLayout(vbox)
		vbox.addWidget(title_label)
		vbox.addWidget(QLabel(description))
		buttons_hbox.addWidget(self.btn)
		vbox.addLayout(buttons_hbox)
		self.setLayout(hbox)

	def download_image_from_url(self, url):
		self.image_downloader = ImageDownloader(url)
		self.image_downloader.image_downloaded.connect(self.update_image)
		self.image_downloader.start()

	def install_module(self):
		self.manager.download_addon(self)

	def update_image(self, pixmap):
		# resize image to 100x100, display it, clean trash
		resized_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
		self.image_label.setPixmap(resized_pixmap)
		del self.image_downloader

	def post_process(self):
		try:
			self.btn2.deleteLater()
			del self.btn2
		except AttributeError:
			self.btn.setText("Uninstall")
			self.btn.pressed.disconnect()
			self.btn.pressed.connect(self.uninstall_module)

	def uninstall_module(self):
		self.manager.delete_addon(self.name)
		if self.git_link is not None:
			self.btn.setText("Install")
			self.btn.pressed.disconnect()
			self.btn.pressed.connect(self.install_module)
		else:
			self.deleteLater()
