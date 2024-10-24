from PyQt5.QtCore import QThread, pyqtSignal
import importlib, shutil, json, sys, git, os


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
        self.get_available_addons()
        self.imported_addons = []  # list with full info about each addon
        self.ia = []  # list with only addon names
        sys.path.append('addons')

        for item in os.listdir('addons/'):
            item_path = os.path.join('addons/', item)

            # Check if it's a package, and import it
            if os.path.isdir(item_path) and os.path.isfile(os.path.join(item_path, "__init__.py")):
                self.import_addon(item)

    def get_available_addons(self):
        self.available_addons = [
            {"name": "useless_addon", "description": "I AM NOT A MORON", "img_url": "https://cdn2.hubspot.net/hubfs/53/image8-2.jpg", "git_link": "https://github.com/ndrnmnk/t", "version": 1.1}
        ]


    def download_addon(self, caller_widget):
        self.git_clone_thread = GitClone(caller_widget.git_link, f"addons/{caller_widget.name}")
        self.git_clone_thread.cloned_successfully.connect(lambda: self.after_downloading_addon(caller_widget))
        self.git_clone_thread.start()

    def import_addon(self, addon_name):
        with open(f"addons/{addon_name}/info.json", "r") as file:
            data = json.loads(file.read())
            data.update({"installed": 1})
            print(data)
        self.ia.append(addon_name)
        self.imported_addons.append(data)
        imported_module = importlib.import_module(addon_name)
        globals()[addon_name] = imported_module

    def delete_addon(self, addon_name):
        index = self.ia.index(addon_name)
        self.ia.pop(index)
        self.imported_addons.pop(index)
        shutil.rmtree(f"addons/{addon_name}")

    def after_downloading_addon(self, caller_widget):
        self.import_addon(caller_widget.name)
        caller_widget.set_btn_uninstall()
        del self.git_clone_thread
