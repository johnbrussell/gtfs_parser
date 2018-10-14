import json


def load_configuration():
    with open("configuration.json") as config_file:
        config = json.load(config_file)
    return config