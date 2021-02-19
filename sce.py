from flask import Blueprint, render_template

sce_bp = Blueprint('sce', __name__, template_folder='templates', url_prefix='/sce')


@sce_bp.route("/")
def index():
    return render_template('index.html')
