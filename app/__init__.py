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

    @app.route('/')
    def index():
        if g.db_conn:
            return "Connexion à la base OK !"
        else:
            return "Pas de connexion à la base."

    return app
