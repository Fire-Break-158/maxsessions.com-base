##
## Library Imports
##

# Standard library imports
import os
import importlib

# Third-party imports


# Import blueprints
def get_blueprints():
    path = "./app/blueprints"
    ignore_dirs = {"__pycache__"}
    directories = [
                    entry.name for entry in os.scandir(path)
                    if entry.is_dir() and entry.name not in ignore_dirs
                    ]
    print(directories)
    return(directories)

def register_blueprint(app):
    blueprints = get_blueprints()

    for blueprint in blueprints:
        try:
            module_path = f"app.blueprints.{blueprint}"
            blueprint_module = importlib.import_module(f"{module_path}.{blueprint}")
            print(f'imported blueprint {blueprint}')
        except ModuleNotFoundError as e:
            print(f"Error importing blueprint {blueprint}: {e}")