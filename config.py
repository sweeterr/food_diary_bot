import yaml


CONFIG_FILE = "config.yml"


class Config:
    def __init__(self, config_file=CONFIG_FILE):
        self.config_file = config_file
        self.bot = {}
        self.google = {}
        self.get_config()

    def get_config(self):
        with open(self.config_file, "r") as file:
            config = yaml.load(file, Loader=yaml.Loader)
        self.bot = config["bot"]
        self.google = config["google"]
