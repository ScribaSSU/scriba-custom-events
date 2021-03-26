import yaml
from flask import Flask

with open("config.yaml") as file:
    config = yaml.safe_load(file)

db_conf = config["database"]
log_conf = config["logging"]

with open("vk_app_config.yaml") as file:
    vk_app_config = yaml.safe_load(file)
vk_conf = vk_app_config["settings"]

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_conf['user']}:{db_conf['password']}@{db_conf['host']}:{db_conf['port']}/{db_conf['db_name']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = db_conf['track_modifications']
app.config['SECRET_KEY'] = vk_conf['client_secret']
