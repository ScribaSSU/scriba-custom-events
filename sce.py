import flask

sce_bp = flask.Blueprint('sce', __name__, template_folder='templates', url_prefix='/sce')

@sce_bp.route("/")
def index():
    return flask.render_template('index.html')
