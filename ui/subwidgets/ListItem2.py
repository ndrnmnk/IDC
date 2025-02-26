from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QTextBrowser
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from io import BytesIO
import requests
from backend.config_manager import ConfigManager


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
	def __init__(self, manager, name, description, categories=None, img_url=None, git_link=None):
		super().__init__()

		if categories is None:
			categories = []
		self.setMaximumHeight(200)
		self.manager = manager
		self.git_link = git_link
		self.name = name
		self.categories = categories

		hbox = QHBoxLayout()
		vbox = QVBoxLayout()
		buttons_hbox = QHBoxLayout()
		hbox.setAlignment(Qt.AlignLeft)
		vbox.setAlignment(Qt.AlignTop)
		buttons_hbox.setAlignment(Qt.AlignLeft)

		# set placeholder image while trying to load actual logo
		self.image_label = QLabel()
		self.image_label.setFixedWidth(100)
		placeholder_pixmap = QPixmap("textures/images/logo.png")
		self.image_label.setPixmap(placeholder_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
		if img_url:
			self.download_image_from_url(img_url)

		self.btn = QPushButton()
		self.btn.setFixedWidth(64)

		if self.git_link is None or name in self.manager.ia:  # if module is installed
			self.btn.setText("Uninstall")
			self.btn.pressed.connect(self.uninstall_module)
			if "Installed" not in self.categories:
				self.categories.append("Installed")
			if any(d.get("name") == name for d in self.manager.to_update):  # if module can be updated, add a second button
				print(name + " could be updated")
				self.btn2 = QPushButton()
				self.btn2.setText("Update")
				self.btn2.pressed.connect(lambda: self.manager.update_addon(self))
				buttons_hbox.addWidget(self.btn2)
		else:  # if module is not installed, add install button
			self.btn.setText("Install")
			self.btn.pressed.connect(self.install_module)

		if self.git_link is None:  # if no GitHub link, just put text as title
			title_label = QLabel(self.name)
		else:  # if GitHub link is present, hyperlink it to the title
			title_label = QLabel(f"<a href='{git_link}'>{name}</a>")
		title_label.setOpenExternalLinks(True)
		title_label.setStyleSheet("font-size: 14pt;")

		hbox.addWidget(self.image_label)
		hbox.addLayout(vbox)
		vbox.addWidget(title_label)
		self.categories_layout = self.generate_categories_hbox()
		vbox.addLayout(self.categories_layout)

		self.description_browser = QTextBrowser()
		self.description_browser.setReadOnly(True)
		self.description_browser.setHtml(description)
		self.description_browser.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		# self.description_browser.setStyleSheet("background: transparent;")  # transparent bg
		self.description_browser.setMaximumHeight(100)  # i don't know actual available height, but this works

		# Add the description_browser widget to your layout instead of a QLabel
		vbox.addWidget(self.description_browser)

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
			if "Installed" not in self.categories:
				self.categories.append("Installed")
			self.update_categories_layout()
			self.btn.setText("Uninstall")
			self.btn.pressed.disconnect()
			self.btn.pressed.connect(self.uninstall_module)

	def uninstall_module(self):
		self.manager.delete_addon(self.name)
		if self.git_link is not None:
			self.btn.setText("Install")
			self.categories.remove("Installed")
			self.update_categories_layout()
			self.btn.pressed.disconnect()
			self.btn.pressed.connect(self.install_module)
		else:
			self.deleteLater()

	def generate_categories_hbox(self):
		hbox = QHBoxLayout()
		hbox.setAlignment(Qt.AlignLeft)
		for item in self.categories:
			hbox.addWidget(QLabel(
				f"<span style='background-color:{ConfigManager().get_config()['addon_category_colors'][item]};'>{item}</span>"))
		return hbox

	def update_categories_layout(self):
		# Remove old items
		while self.categories_layout.count():
			child = self.categories_layout.takeAt(0)
			if child.widget():
				child.widget().deleteLater()

		# Add new category labels
		for item in self.categories:
			label = QLabel(
				f"<span style='background-color:{ConfigManager().get_config()['addon_category_colors'][item]};'>{item}</span>")
			self.categories_layout.addWidget(label)
