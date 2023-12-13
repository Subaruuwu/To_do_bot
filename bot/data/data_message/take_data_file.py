import os
import json
from typing import Final


def get_data_file():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(current_dir, 'data_file.json')

    with open(data_file_path, 'r', encoding='utf-8') as d_file:
        data_dict = json.loads(d_file.read())
    return data_dict


class DataDict:
    DATAMESSAGE: Final = get_data_file()
