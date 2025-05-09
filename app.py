from flask import Flask, jsonify,request
from werkzeug.security import generate_password_hash
from flask_jwt_extended import JWTManager,create_access_token,jwt_required,get_jwt_identity
import psycopg2


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "codedev"
jwt = JWTManager(app)

# Configuration de la base PostgreSQL
DB_CONFIG = {
    'dbname': 'marchéboubess',
    'user': 'postgres',
    'password': '964Cfxgr@',
    'host': 'localhost',
    'port': '5432'
}

# Connexion simple à PostgreSQL
def get_Connexion():
    return psycopg2.connect(**DB_CONFIG)

# Route publique : liste des produits
@app.route('/prompt', methods=['GET'])
def get_prompt():
    connecter = get_Connexion()
    with connecter.cursor() as cur:
        cur.execute("SELECT id, nom, description, prix FROM Prompts")
        Prompts = cur.fetchall()
        resultat = [
            {"id": p[0], "nom": p[1], "description": p[2], "prix": float(p[3])}
            for p in Prompts
        ]
    connecter.close()
    return jsonify(resultat)




@app.route("/login", methods=["POST"])
def login():
    connecter = get_Connexion()
    nom_user = request.json.get("nom_user")
    motpasse = request.json.get("motpasse")
    
    connecter.execute("SELECT nom_user, motpasse, role approved FROM User WHERE nom_user =%s" ,(nom_user,))
    user=connecter.fetchone()

    if not user:
        return jsonify()
    

if __name__ == '__main__':
    app.run(debug=True)
