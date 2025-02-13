##
## Library Imports
##

# Standard library imports
import os
import importlib

#Third Party Imports


# Import blueprints
def get_blueprints():
    path = "./app/blueprints"
    ignore_dirs = {"__pycache__"}
    directories = [
        entry.name for entry in os.scandir(path)
        if entry.is_dir() and entry.name not in ignore_dirs
    ]
    return directories

def register_blueprint(app):
    global ICON_STYLESHEETS, MENU_ITEMS  # Store once to avoid duplication
    blueprints = get_blueprints()
    ICON_STYLESHEETS = []  # Reset stylesheets on each run
    MENU_ITEMS = []  # Reset menu items on each run

    for blueprint in blueprints:
        try:
            module_path = f"app.blueprints.{blueprint}"
            blueprint_module = importlib.import_module(f"{module_path}.{blueprint}")

            if hasattr(blueprint_module, "bp"):
                app.register_blueprint(blueprint_module.bp, url_prefix=f"/{blueprint}")
                print(f"Imported blueprint: {blueprint}")

                # Collect menu items if defined
                if hasattr(blueprint_module, "MENU_ITEMS"):
                    MENU_ITEMS.extend(blueprint_module.MENU_ITEMS)

                    # Dynamically find `icons.css`
                    icons_css_path = f"/{blueprint}/static/css/icons.css"
                    full_path = f"app/blueprints/{blueprint}/static/css/icons.css"
                    if os.path.exists(full_path):
                        ICON_STYLESHEETS.append(icons_css_path)  # Store dynamically
                        print(f"✔ Found icons.css for {blueprint}: {icons_css_path}")  # Debugging Output
                    else:
                        print('No icon.css found to use as a stylesheet.')

            else:
                print(f"Warning: No `bp` found in {blueprint}")

        except ModuleNotFoundError as e:
            print(f"Error importing blueprint {blueprint}: {e}")

def get_blueprint_stylesheets():
    return ICON_STYLESHEETS  # Allow retrieval of stored stylesheets

def get_blueprint_menu_items():
    return MENU_ITEMS  