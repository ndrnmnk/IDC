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

info.json must contain something like this:

```json
{
  "name": "Addon_name_that_uses_underscores_as_spaces",
  "description": "Description of addon (required)",
  "img_url": "link.to/logo-of-addon, or None",
  "git_link": "link.to/git-repo-of-addon, or None",
  "version": 1.0
}
```

And `__init__.py` must contain `run(ui)` function, which will start the module. Here is an example:

```python
def run(ui):
    ui.setStyleSheet("background-color: lightgray;")
```

And that's it! Go create your own addons!