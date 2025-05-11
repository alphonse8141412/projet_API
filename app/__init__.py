from app.routes.client import client_bp
from app.routes.groupes import groupes_bp
from app.routes.prompt import prompt_bp
from flask import Flask, g
import psycopg2
from config.configuration import load_config


def create_app():
    app = Flask(__name__)
    config = load_config()

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

    return app
