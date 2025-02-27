from PyQt5.QtWidgets import (
    QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QTextBrowser
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from io import BytesIO
import requests
from backend.config_manager import ConfigManager


class ImageDownloader(QThread):
    """
    A QThread subclass that downloads an image from a given URL and emits
    a QPixmap via the 'image_downloaded' signal.
    """
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
    """
    Widget representing a single addon item with image, title, description,
    category labels, and an install/uninstall button (with an optional update button).
    """
    def __init__(self, manager, name, description, categories=None, img_url=None, git_link=None):
        super().__init__()
        if categories is None:
            categories = []
        self.setMaximumHeight(200)

        # Store parameters
        self.manager = manager
        self.git_link = git_link
        self.name = name
        self.categories = categories  # List of category strings

        # Create and configure layouts
        self.main_hbox = QHBoxLayout()
        self.main_vbox = QVBoxLayout()
        self.buttons_hbox = QHBoxLayout()
        self.main_hbox.setAlignment(Qt.AlignLeft)
        self.main_vbox.setAlignment(Qt.AlignTop)
        self.buttons_hbox.setAlignment(Qt.AlignLeft)

        # Initialize UI components
        self._init_image_label(img_url)
        self._init_action_button()
        title_label = self._create_title_label()
        self.main_vbox.addWidget(title_label)

        # Create and add category labels layout
        self.categories_layout = QHBoxLayout()
        self.categories_layout.setAlignment(Qt.AlignLeft)
        self.main_vbox.addLayout(self.categories_layout)
        self.update_categories_layout()

        # Create description browser for detailed text
        self.description_browser = QTextBrowser()
        self.description_browser.setReadOnly(True)
        self.description_browser.setHtml(description)
        self.description_browser.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.description_browser.setMaximumHeight(100)
        self.main_vbox.addWidget(self.description_browser)

        # Add action button(s)
        self.buttons_hbox.addWidget(self.btn)
        # If update button was created, it would have been added already
        self.main_vbox.addLayout(self.buttons_hbox)

        self.main_hbox.addWidget(self.image_label)
        self.main_hbox.addLayout(self.main_vbox)
        self.setLayout(self.main_hbox)

    def _init_image_label(self, img_url):
        """
        Initialize the image label with a placeholder pixmap.
        If an image URL is provided, start the download.
        """
        self.image_label = QLabel()
        self.image_label.setFixedWidth(100)
        placeholder_pixmap = QPixmap("textures/images/logo.png")
        self.image_label.setPixmap(
            placeholder_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )
        if img_url:
            self.download_image_from_url(img_url)

    def _init_action_button(self):
        """
        Initialize the main action button and, if applicable, the update button.
        """
        self.btn = QPushButton()
        self.btn.setFixedWidth(64)

        # If no git link is provided or the module is already installed...
        if self.git_link is None or self.name in self.manager.ia:
            self.btn.setText("Uninstall")
            self.btn.pressed.connect(self.uninstall_module)
            if "Installed" not in self.categories:
                self.categories.append("Installed")
            # If an update is available, add an update button
            if any(d.get("name") == self.name for d in self.manager.to_update):
                print(f"{self.name} could be updated")
                self.update_button = QPushButton("Update")
                self.update_button.pressed.connect(lambda: self.manager.update_addon(self))
                self.buttons_hbox.addWidget(self.update_button)
        else:
            self.btn.setText("Install")
            self.btn.pressed.connect(self.install_module)

    def _create_title_label(self):
        """
        Create a QLabel for the title. If a GitHub link is provided,
        make the title a clickable hyperlink.
        """
        if self.git_link is None:
            title_label = QLabel(self.name)
        else:
            title_label = QLabel(f"<a href='{self.git_link}'>{self.name}</a>")
            title_label.setOpenExternalLinks(True)
        title_label.setStyleSheet("font-size: 14pt;")
        return title_label

    def download_image_from_url(self, url):
        """
        Download an image from the provided URL using ImageDownloader.
        """
        self.image_downloader = ImageDownloader(url)
        self.image_downloader.image_downloaded.connect(self.update_image)
        self.image_downloader.start()

    def install_module(self):
        """Trigger the installation process via the manager."""
        self.manager.download_addon(self)

    def update_image(self, pixmap):
        """
        Resize the downloaded pixmap and update the image label.
        Clean up the downloader afterward.
        """
        resized_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(resized_pixmap)
        self.image_downloader = None

    def post_process(self):
        """
        Update the UI after an update operation.
        If an update button exists, remove it. Otherwise, update the category list
        and change the button to "Uninstall".
        """
        try:
            self.update_button.deleteLater()
            del self.update_button
        except AttributeError:
            self.categories.append("Installed")
            self.update_categories_layout()
            self.btn.setText("Uninstall")
            self.btn.pressed.disconnect()
            self.btn.pressed.connect(self.uninstall_module)

    def uninstall_module(self):
        """
        Trigger the uninstallation process via the manager.
        Adjust the UI based on whether a GitHub link is present.
        """
        self.manager.delete_addon(self.name)
        if self.git_link is not None:
            self.btn.setText("Install")
            try:
                self.categories.remove("Installed")
            except ValueError:
                pass
            self.update_categories_layout()
            self.btn.pressed.disconnect()
            self.btn.pressed.connect(self.install_module)
        else:
            self.deleteLater()

    def update_categories_layout(self):
        """Remove all existing category labels from the layout and repopulate it."""
        # Clear existing items from the layout
        while self.categories_layout.count():
            child = self.categories_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        # Add updated category labels
        config = ConfigManager().get_config()
        for item in self.categories:
            label = QLabel(f"<span style='background-color:{config['addon_category_colors'][item]};'>{item}</span>")
            self.categories_layout.addWidget(label)
