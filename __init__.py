from flask import Flask, redirect, url_for, json
from burnin.database import db_session
from burnin.models import User

application = Flask(__name__)

application.config.from_object(__name__)
application.config.update(dict(
    JSONIFY_PRETTYPRINT_REGULAR=False
))
application.config.from_envvar('FLASK_SERVER_SETTINGS', silent=True)

@application.teardown_appcontext
def shutdown_dbsession(exception=None):
    db_session.remove()

@application.route('/')
def index():
    return redirect(url_for('users'))

@application.route('/api/users')
def users():
    users = db_session.query(User).all()
    return json.jsonify([user.to_dict() for user in users])