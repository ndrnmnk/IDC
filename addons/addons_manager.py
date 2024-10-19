import sys
import os
import importlib


def addons_manager(ui):
    # Step 1: Add the directory containing your packages/modules to the system path
    module_dir = 'addons/'
    sys.path.append(module_dir)

    # Step 2: Iterate through all files and directories in the module directory
    for item in os.listdir(module_dir):
        item_path = os.path.join(module_dir, item)

        # Check if it's a package (directory with __init__.py)
        if os.path.isdir(item_path) and os.path.isfile(os.path.join(item_path, "__init__.py")):
            # Import the package by its directory name
            print(item)
            imported_module = importlib.import_module(item)
            globals()[item] = imported_module

        # If it's a single .py file (but not __init__.py), import it
        elif item.endswith(".py") and item != "__init__.py" and item != "addons_manager.py":
            print(item)
            module_name = item[:-3]  # Strip the ".py" extension
            imported_module = importlib.import_module(module_name)
            globals()[module_name] = imported_module

    print("All modules and packages imported successfully!")
