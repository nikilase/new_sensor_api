from os.path import dirname, join

from fastapi.templating import Jinja2Templates

current_dir = dirname(__file__)  # this will be the location of the current .py file
view_folder = join(current_dir, "views")

favicon_path = join(current_dir, "static/favicon.ico")

templates = Jinja2Templates(directory=view_folder)
