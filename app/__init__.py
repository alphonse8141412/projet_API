from app.routes.client import client_bp
from app.routes.groupes import groupes_bp
from app.routes.prompt import prompt_bp
from app.routes.achats import achats_bp
from app.routes.votes import votes_bp
from app.routes.notes import notes_bp
from app.routes.auth import auth_bp

from flask_jwt_extended import JWTManager
from flask import Flask, g
import psycopg2
from config.configuration import load_config


def create_app():
    app = Flask(__name__)
    config = load_config()

   # Clé secrète pour signer les JWT (à changer en production)
    app.config["JWT_SECRET_KEY"] = "super-secret-key"

    jwt = JWTManager(app)

    @app.before_request
    def before_request():
        try:
            g.db_conn = psycopg2.connect(**config)
        except Exception as e:
            print("Erreur connexion DB :", e)
            g.db_conn = None

    @app.teardown_request
    def teardown_request(exception):
        db_conn = getattr(g, 'db_conn', None)
        if db_conn is not None:
            db_conn.close()

    app.register_blueprint(client_bp)
    app.register_blueprint(groupes_bp)
    app.register_blueprint(prompt_bp)
    app.register_blueprint(achats_bp)
    app.register_blueprint(notes_bp)
    app.register_blueprint(votes_bp)
    app.register_blueprint(auth_bp)

    return app
