import json
import os

ROOT_PATH = os.path.dirname(__file__)

CONFIG_FILE_PATH = os.path.join(ROOT_PATH, 'appsettings.json')

if os.path.exists(CONFIG_FILE_PATH):
    with open(CONFIG_FILE_PATH, 'r') as r_file:
        data = json.load(r_file)
        r_file.close()
else:
    data = dict()

MONGO_CONNECTION_STRING = data.get('mongo_connection_string', 'mongodb://localhost:31279')

SECRET_KEY = data.get('secret_key', 'secret_key')