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

            # Convert the image to QPixmap
            image_data = BytesIO(response.content)
            pixmap = QPixmap()
            pixmap.loadFromData(image_data.read())

            # Emit the signal with the QPixmap
            self.image_downloaded.emit(pixmap)

        except Exception as e:
            print(f"Error downloading image: {e}")


class ListItem(QWidget):
    def __init__(self, parent, title, description, img_path=None, git_link=None):
        super().__init__()
        self.parent = parent
        self.git_link = git_link
        if self.git_link is None:
            self.title = title
            self.installed = True
        else:
            self.title = f"<a href='{git_link}'>{title}</a>"
            self.installed = self.title in parent.addons_manager.imported_addons

        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        hbox.setAlignment(Qt.AlignLeft)
        vbox.setAlignment(Qt.AlignTop)

        self.image_label = QLabel()

        # Set a placeholder image initially from disk
        placeholder_pixmap = QPixmap("textures/logo.png")
        self.image_label.setPixmap(placeholder_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        if img_path:
            self.download_image_from_url(img_path)

        if not self.installed:
            self.btn = QPushButton("Install")
            self.btn.pressed.connect(self.install_module)
            self.btn.setFixedWidth(50)
        else:
            self.btn = QPushButton("Uninstall")
            self.btn.pressed.connect(self.uninstall_module)
            self.btn.setFixedWidth(64)

        title_label = QLabel(self.title)
        title_label.setOpenExternalLinks(True)
        title_label.setStyleSheet("font-size: 14pt;")

        hbox.addWidget(self.image_label)
        hbox.addLayout(vbox)
        vbox.addWidget(title_label)
        vbox.addWidget(QLabel(description))
        vbox.addWidget(self.btn)
        self.setLayout(hbox)

    def download_image_from_url(self, url):
        # Create a QThread to download the image without blocking the UI
        self.image_downloader = ImageDownloader(url)
        self.image_downloader.image_downloaded.connect(self.update_image)
        self.image_downloader.start()

    def update_image(self, pixmap):
        # Resize the image to 100x100 pixels
        resized_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(resized_pixmap)

    def install_module(self):
        print("not implemented yet")
        self.btn.setText("Uninstall")
        self.btn.setFixedWidth(64)
        self.btn.pressed.disconnect()
        self.btn.pressed.connect(self.uninstall_module)

    def uninstall_module(self):
        self.parent.addons_manager.delete_addon(self.title)
        self.btn.setText("Install")
        self.btn.setFixedWidth(50)
        self.btn.pressed.disconnect()
        self.btn.pressed.connect(self.install_module)
