from flask import Flask
from flask.blueprints import Blueprint
import config
from models import db
import routes


app = Flask(__name__)
app.debug = config.DEBUG
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URI
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
