import os
from app import create_app
from config import default
settings_module = os.getenv("APP_SETTINGS_MODULE")
app = create_app(default)
print(settings_module)