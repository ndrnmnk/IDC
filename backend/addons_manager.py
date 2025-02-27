from PyQt5.QtWidgets import QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import importlib, shutil, json, sys, git, os
from backend.config_manager import ConfigManager


def find_matching_indices(list1, list2):
    """Return list of (index1, index2) tuples for entries with matching 'name' fields."""
    mapping = {item['name']: idx for idx, item in enumerate(list1)}
    return [(mapping[item['name']], idx) for idx, item in enumerate(list2) if item['name'] in mapping]


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
        self.imported_addons = []  # full addon info dicts
        self.ia = []             # addon names only
        self.to_update = []      # addons with updates available
        self.with_options = []   # addons that provide options widgets

        self.addons_dir = 'addons'
        sys.path.append(self.addons_dir)
        os.makedirs(self.addons_dir, exist_ok=True)

        self._load_installed_addons()
        self.get_available_addons()
        self.check_addon_updates()

    def _load_installed_addons(self):
        """Import all installed addons from the addons directory."""
        for item in os.listdir(self.addons_dir):
            item_path = os.path.join(self.addons_dir, item)
            if os.path.isdir(item_path) and os.path.isfile(os.path.join(item_path, "__init__.py")):
                self.import_addon(item)

    def get_available_addons(self):
        """Placeholder: Define available addons (would normally be fetched from an online source)."""
        self.available_addons = [
            {
                "name": "useless_addon",
                "description": "Test addon which has a Google logo",
                "img_url": "https://cdn2.hubspot.net/hubfs/53/image8-2.jpg",
                "git_link": "https://github.com/ndrnmnk/t",
                "version": 1.0,
                "categories": ["Others"]
            }
        ]

    def check_addon_updates(self):
        """Compare installed addons with available ones to determine if updates exist."""
        for idx1, idx2 in find_matching_indices(self.imported_addons, self.available_addons):
            if self.imported_addons[idx1]["version"] < self.available_addons[idx2]["version"]:
                self.to_update.append(self.imported_addons[idx1])
        if self.to_update:
            print("Found addon updates")
            if ConfigManager().get_config().get("autoupdate_addons", False):
                for addon in self.to_update:
                    self.update_addon(addon)

    def _get_widget_info(self, caller):
        """
        Normalizes caller so that we always have a dict with keys:
        'name', 'git_link', and an optional 'post_process' callable.
        """
        if isinstance(caller, dict):
            return caller
        return {
            "name": getattr(caller, "name", None),
            "git_link": getattr(caller, "git_link", None),
            "post_process": getattr(caller, "post_process", lambda: None)
        }

    def download_addon(self, caller):
        """Download an addon via GitClone and proceed to import it after cloning."""
        info = self._get_widget_info(caller)
        addon_path = os.path.join(self.addons_dir, info["name"])
        self.git_clone_thread = GitClone(info["git_link"], addon_path)
        self.git_clone_thread.cloned_successfully.connect(lambda: self.after_downloading_addon(caller))
        self.git_clone_thread.start()

    def import_addon(self, addon_name):
        """Import an addon by reading its info.json and executing its run() method."""
        info_file = os.path.join(self.addons_dir, addon_name, "info.json")
        with open(info_file, "r") as file:
            data = json.load(file)
        data["installed"] = True
        self.ia.append(addon_name)
        self.imported_addons.append(data)
        imported_module = importlib.import_module(addon_name)
        imported_module.run(self.ui)
        if data.get("has_options"):
            self.with_options.append(imported_module)
        globals()[addon_name] = imported_module

    def delete_addon(self, addon_name):
        """Remove addon from internal lists and delete its folder."""
        if addon_name in self.ia:
            self.ia.remove(addon_name)
        self.imported_addons = [a for a in self.imported_addons if a["name"] != addon_name]
        shutil.rmtree(os.path.join(self.addons_dir, addon_name), ignore_errors=True)

    def update_addon(self, caller):
        """Update an addon by deleting the current one and downloading it anew."""
        info = self._get_widget_info(caller)
        self.delete_addon(info["name"])
        self.download_addon(caller)

    def after_downloading_addon(self, caller):
        """
        After a successful download, import the addon, execute its post_process method if available,
        and remove the addon from the update list regardless of the caller_widget type.
        """
        info = self._get_widget_info(caller)
        addon_name = info["name"]

        self.import_addon(addon_name)

        # Call post_process if it exists (works for non-dict caller_widget)
        if not isinstance(caller, dict):
            getattr(caller, "post_process", lambda: None)()

        # Remove any entry with this addon name from the update list
        self.to_update = [upd for upd in self.to_update if upd.get("name") != addon_name]

        self.git_clone_thread = None

    def get_options(self):
        """Generate a QVBoxLayout containing options widgets for each addon that provides them."""
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        for module in self.with_options:
            label = QLabel(f"{module.__name__}:")
            label.setStyleSheet("font-size: 14pt;")
            layout.addWidget(label)
            layout.addWidget(module.options_widget())
        return layout
