from flask import Flask
from flask_cors import CORS
from extensions import db, mail, jwt
from config import Config
from routes.auth_routes import auth as auth_routes
from routes.main_routes import main as main_routes



def start_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Extensions
    CORS(app)
    db.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)

    # Blueprints
    app.register_blueprint(auth_routes, url_prefix='/api/auth')
    app.register_blueprint(main_routes, url_prefix='/api')

    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = start_app()
    app.run(debug=True)