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
  "version": 1.0,
  "has_options": true
}
```

And `__init__.py` must contain `run(ui)` function, which will start the module. Here is an example:

```python
def run(ui):
    ui.setStyleSheet("background-color: lightgray;")

def options_widget():
    # this function is required only if "has_options" is true in info.json
    return QLabel("this label was made using example addon")
```

And that's it! Now you can create your own addons!