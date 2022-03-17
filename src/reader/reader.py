import json


def read(file_name):
    try:
        with open(file_name, 'r') as file:
            data = json.load(file)

        return data
    except Exception:
        raise
