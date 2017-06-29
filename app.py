from flask import Flask
from flask.blueprints import Blueprint
import config
from config import celery
from models import db
import routes

app = Flask(__name__)
app.debug = config.DEBUG
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URI
app.config['CELERY_BROKER_URL'] = config.SQS_URI
app.config['result_backend'] = 'rpc://'
app.config['broker_transport_options'] = config.SQS_OPTIONS

celery.conf.update(app.config)
db.init_app(app)
db.app = app

for blueprint in vars(routes).values():
    if isinstance(blueprint, Blueprint):
        app.register_blueprint(
            blueprint,
            url_prefix=""
        )

if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT)
