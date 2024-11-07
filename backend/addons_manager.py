from PyQt5.QtWidgets import QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread, pyqtSignal
import importlib, shutil, json, sys, git, os


def find_matching_indices(list1, list2):
	# Create a dictionary from the first list with name as key and index as value
	dict1 = {item['name']: idx for idx, item in enumerate(list1)}

	# Find matching "name" fields and collect their indices
	matching_indices = []
	for idx2, item in enumerate(list2):
		name = item['name']
		if name in dict1:
			# Append a tuple of (index from list1, index from list2) where names match
			matching_indices.append((dict1[name], idx2))

	return matching_indices


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
		self.ui = ui

		self.imported_addons = []  # list with full info about each addon
		self.ia = []  # list with only addon names
		self.to_update = []  # list of addons with updates available
		self.with_options = []

		sys.path.append('addons')

		for item in os.listdir('addons/'):
			item_path = os.path.join('addons/', item)

			# Check if it's a package, and import it
			if os.path.isdir(item_path) and os.path.isfile(os.path.join(item_path, "__init__.py")):
				self.import_addon(item)
		self.check_addons_updates()

	def get_available_addons(self):
		self.available_addons = [
			{"name": "useless_addon", "description": "I AM NOT A MORON", "img_url": "https://cdn2.hubspot.net/hubfs/53/image8-2.jpg", "git_link": "https://github.com/ndrnmnk/t", "version": 1.0}
		]

	def download_addon(self, caller_widget):
		self.git_clone_thread = GitClone(caller_widget.git_link, f"addons/{caller_widget.name}")
		self.git_clone_thread.cloned_successfully.connect(lambda: self.after_downloading_addon(caller_widget))
		self.git_clone_thread.start()

	def import_addon(self, addon_name):
		with open(f"addons/{addon_name}/info.json", "r") as file:
			data = json.loads(file.read())
		data.update({"installed": 1})
		self.ia.append(addon_name)
		self.imported_addons.append(data)
		imported_module = importlib.import_module(addon_name)
		imported_module.run(self.ui)

		if data["has_options"]:
			self.with_options.append(imported_module)

		globals()[addon_name] = imported_module

	def delete_addon(self, addon_name):
		index = self.ia.index(addon_name)
		self.ia.pop(index)
		self.imported_addons.pop(index)
		shutil.rmtree(f"addons/{addon_name}")

	def after_downloading_addon(self, caller_widget):
		self.import_addon(caller_widget.name)
		caller_widget.post_process()
		del self.git_clone_thread

	def check_addons_updates(self):
		possible_updates = find_matching_indices(self.imported_addons, self.available_addons)
		for item in possible_updates:
			if self.imported_addons[item[0]]["version"] < self.available_addons[item[1]]["version"]:
				self.to_update.append(self.imported_addons[item[0]]["name"])
		if self.to_update:
			print(f"found addon updates: {self.to_update}")

	def update_addon(self, caller_widget):
		self.delete_addon(caller_widget.name)
		self.download_addon(caller_widget)

	def get_options(self):
		vbox = QVBoxLayout()
		vbox.setAlignment(Qt.AlignTop)
		for item in self.with_options:
			label = QLabel(f"{item.__name__}:")
			label.setStyleSheet("font-size: 14pt;")
			vbox.addWidget(label)
			vbox.addWidget(item.options_widget())
		return vbox
