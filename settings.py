import yaml
from flask import Flask

with open("config.yaml") as file:
    config = yaml.safe_load(file)
db_conf = config["database"]
log_conf = config["logging"]

try:
    with open("vk_app_config.yaml") as file:
        vk_app_config = yaml.safe_load(file)
    vk_conf = vk_app_config["settings"]
except FileNotFoundError:
    vk_conf = {"client_id": 123123123,
               "client_secret": "aaBBccDD",
               "redirect_uri": "http://redirect_uri-custom-events.ru/vk_auth"}

app = Flask(__name__)