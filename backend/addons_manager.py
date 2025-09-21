from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import importlib, shutil, json, git, os
from backend.config_manager import ConfigManager


class GitClone(QThread):
    cloned_successfully = pyqtSignal()

    def __init__(self, url, path):
        super().__init__()
        self.url = url
        self.path = path

    def run(self):
        try:
            git.Repo.clone_from(self.url, self.path)
            self.cloned_successfully.emit()
        except Exception as e:
            print(f"Error downloading image: {e}")


class AddonsManager:
    def __init__(self, ui):
        self.ui = ui
        self.addons_names = []
        self.addons = {}
        self.addons_metadata = {}
        self.available_addons = self.get_available_addons()
        self.load_installed_addons()

    def load_installed_addons(self):
        for item in os.listdir("addons"):
            item_path = os.path.join("addons", item)
            if os.path.isdir(item_path) and os.path.isfile(os.path.join(item_path, "__init__.py")):
                self.import_addon(item)

    def import_addon(self, addon_name):
        with open(os.path.join("addons", addon_name, "info.json"), "r") as file:
            self.addons_metadata[addon_name] = json.load(file)

        if addon_name in self.available_addons and self.available_addons[addon_name]["version"] > self.addons_metadata[addon_name]["version"]:
            print(f"{addon_name} can be updated")
            self.addons_metadata[addon_name]["updates_available"] = True
            if ConfigManager().get_config()["autoupdate_addons"]:
                self.update_addon(addon_name)

        imported_module = importlib.import_module(f"addons.{addon_name}")
        self.addons[addon_name] = imported_module.run(self.ui, os.path.join("addons", addon_name))

        self.addons_names.append(addon_name)

    def delete_addon(self, addon_name, caller_widget=None):
        if self.addons[addon_name].on_delete() is True:
            shutil.rmtree(os.path.join("addons", addon_name), ignore_errors=True)
            self.addons_names.remove(addon_name)
            del self.addons_metadata[addon_name]
            del self.addons[addon_name]
            if caller_widget:
                caller_widget.post_process(0)
        else:
            print(f"Could not delete addon: {addon_name}")

    def download_addon_step1(self, addon_name, caller_widget=None, update_addon=False):
        self.git_clone_thread = GitClone(self.available_addons[addon_name]["git_link"], os.path.join("addons", addon_name))
        self.git_clone_thread.cloned_successfully.connect(lambda n=addon_name, cw=caller_widget, ua=update_addon: self.download_addon_step2(n, cw, ua))
        self.git_clone_thread.start()

    def download_addon_step2(self, addon_name, caller_widget, update_addon):
        self.import_addon(addon_name)
        if caller_widget:
            caller_widget.post_process(1+update_addon)

    def update_addon(self, addon_name, caller_widget=None):
        print(f"updating addon: {addon_name}")
        self.delete_addon(addon_name)
        self.download_addon_step1(addon_name, caller_widget, True)

    def get_available_addons(self):
        return {
            "useless_addon": {
                "name": "useless_addon",
                "description": "Test addon which has a Google logo",
                "img_url": "https://cdn2.hubspot.net/hubfs/53/image8-2.jpg",
                "git_link": "https://github.com/ndrnmnk/t",
                "version": 1.0,
                "categories": ["Others"]
            }
        }

    def get_options(self):
        print("get options")
        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignTop)
        for addon in self.addons_names:
            if self.addons_metadata[addon]["has_options"]:
                vbox.addWidget(self.addons[addon].on_options())
        return vbox
