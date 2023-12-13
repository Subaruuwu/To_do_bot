from typing import Final
import json
import os


def take_config_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(current_dir, 'configuration_file.json')

    with open(config_file_path, 'r') as config_file:
        config = json.loads(config_file.read())
    return config


def take_token():
    config = take_config_data()
    token = config['configuration']['TOKEN']
    return token


class TgKeys:
    TOKEN: Final = take_token()
