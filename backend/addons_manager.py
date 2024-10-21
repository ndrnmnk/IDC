import shutil
import sys
import os
import importlib


class AddonsManager:
    def __init__(self, ui):
        # Step 1: Add the directory containing your packages/modules to the system path
        self.imported_addons = []
        sys.path.append('addons')

        # Step 2: Iterate through all files and directories in the module directory
        for item in os.listdir('addons/'):
            item_path = os.path.join('addons/', item)

            # Check if it's a package (directory with __init__.py)
            if os.path.isdir(item_path) and os.path.isfile(os.path.join(item_path, "__init__.py")):
                self.import_addon(item)


        print(self.imported_addons)

    def import_addon(self, addon_name):
        self.imported_addons.append(addon_name)
        imported_module = importlib.import_module(addon_name)
        globals()[addon_name] = imported_module

    def delete_addon(self, addon_name):
        self.imported_addons.remove(addon_name)
        shutil.rmtree(f"addons/{addon_name}")
