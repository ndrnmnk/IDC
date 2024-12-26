import json


class ConfigManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ConfigManager, cls).__new__(cls, *args, **kwargs)
            cls._instance.config = {}
            cls._instance.blocks = {}
            cls._instance.config_file_path = None
        return cls._instance

    def load_config(self, file_path):
        self.config_file_path = file_path
        with open(file_path, 'r') as file:
            self.config = json.load(file)

    def load_blocks(self, file_path):
        with open(file_path, 'r') as file:
            self.blocks = json.load(file)

    def get_config(self, key, default=None):
        return self.config.get(key, default)

    def get_blocks(self, key, default=None):
        if key is not 0:
            return self.blocks.get(key, default)
        return self.blocks

    def set(self, key, value):
        if isinstance(key, list):  # if key is list, edit nested jsons
            config = self.config
            for k in key[:-1]:
                config = config[k]
            config[key[-1]] = value  # Set the final key to the value
        else:
            self.config[key] = value

    def save_config(self):
        if self.config_file_path:
            with open(self.config_file_path, 'w') as file:
                json.dump(self.config, file, indent=4)
