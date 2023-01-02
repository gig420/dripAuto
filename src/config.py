'''
    - config.py
'''

import os
import toml
import src.constants as con

class Config:
    def __init__(self):
        self.config_file = os.path.join(con.DIR_CFG, con.FILE_CFG)
        self.config = {}
        self.load()

    def load(self):
        """Load the configuration from the config file."""
        with open(self.config_file, 'r') as f:
            self.config = toml.load(f)

    def save(self):
        """Save the configuration to the config file."""
        with open(self.config_file, 'w') as f:
            toml.dump(self.config, f)

    def get(self, key, value=None):
        """Get the value of a config key."""
        if key in self.config:
            if value is not None:
                return self.config[key][value]
            else:
                return self.config[key]
        return None

    def set(self, key, key2, value):
        """Set the value of a config key."""
        self.config[key][key2] = value
        self.save()