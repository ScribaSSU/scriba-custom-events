from flask import Flask
from sce import sce_bp

app = Flask(__name__)
app.register_blueprint(sce_bp, url_prefix='/sce')


if __name__ == '__main__':
    app.run()
