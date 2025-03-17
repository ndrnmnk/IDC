# TUTORIALS

## Setup

### Step 1: Clone

You can download repository as zip and extract it, or use this command:

```shell
git clone https://github.com/ndrnmnk/IDC
```

### Step 2: Install dependencies

Main dependency of IDC is [Python](https://www.python.org/), after installing it use this command in directory where you cloned IDC:

```shell
pip3 install -r requirements.txt
```

### Step 3: Code

Well, it should work, if it doesn't, open an issue

## Creating addons

### General structure:

Addons must contain these files:

```
.
└──example_addon
   ├── info.json
   └──__init__.py
```

Where `info.json` must contain something like this:

```json
{
  "name": "Addon_name_in_snake_style",
  "description": "Description of an addon (required)",
  "img_url": "example.com/link-to-logo-of-addon, or None",
  "git_link": "example.com/link-to-git-repo-of-addon, or None",
  "categories": ["ListOfCategories"],
  "version": 1.0,
  "has_options": true
}
```

And `__init__.py` must contain `run(ui)` function, which will return an addon class. Addon class must inherit from 
BaseAddon (check `backend/BaseAddon.py` to see which functions can be overridden). Here is an example:

```python
from backend.BaseAddon import BaseAddon
from PyQt5.QtWidgets import QLabel


class ExampleAddonClassName(BaseAddon):
	def init(self):
		print("hi there")

	def on_options(self):
		return QLabel("This label will appear in options")
	
	def on_delete(self):
		print("why do you delete me(")
		return True  # if returns false, module won't be removed; DON'T ABUSE THIS

	def on_idc_close(self):
		print("bye!")


def run(ui):
	return ExampleAddonClassName(ui)
```

And that's it! Now you can create your own addons!

### Creating compiler addons

If you are making a compiler addon, you must follow these rules:

    - babyproof everything
    - don't let compilation fail if the issue wasn't displayed in problems tab
    - don't generate unreadable code (no "all code in one line" etc.)
    - don't specifically slow down the generated code or compilation process
    - no leaving backdoors / integrating malware etc.

Now, lets start. To get current blocks, use this: ```self.ui.code_tab.get_data(False)```

When you need to get current project folder, use ```self.ui.opened_project_path```

Also, you can get path to your addon folder with ```self.folder_name```

The rest lies on YOU!