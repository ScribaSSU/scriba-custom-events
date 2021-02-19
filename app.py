from flask import Flask
from sce import sce_bp
from settings import config

import logging

app = Flask(__name__)
app.register_blueprint(sce_bp)

logging.basicConfig(level=config['logging']['level'])

if __name__ == '__main__':
    app.run()
