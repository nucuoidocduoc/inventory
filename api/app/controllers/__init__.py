import os
import platform
import string
import importlib
import inspect
from flask import Flask, Blueprint, current_app as app

def get_slash_form() -> string:
    slash = "\\"
    if platform.system() == "Windows":
        slash ="\\"
    elif platform.system() == "Linux":
        slash ="/"
    elif platform.system() == "Darwin":
        slash ="/"
    return slash

slash = get_slash_form()

def register_api(app: Flask): 
    register_api_in_folder(app, f"app{slash}controllers")

def register_api_in_folder(app: Flask, folder_path: string):
    for (root, dirs, files) in os.walk(folder_path, topdown=True):
        if len(files) > 0:
            for file in files:
                if file.endswith('.py'):
                    package = f"{folder_path}{slash}{file}".split(".")[0]
                    module_name = file.split(".")[0]
                    module = importlib.import_module(package.replace(slash, "."))
                    members = inspect.getmembers(module)
                    for member in members:
                        if len(member) == 2 and member[0] == module_name and type(member[1]) == Blueprint:
                            if module_name not in app.blueprints.keys():
                                app.register_blueprint(member[1])  
        if len(dirs) > 0:
            for dir in dirs:
                if dir != "__pycache__":
                    register_api_in_folder(app, f"{folder_path}{slash}{dir}") 