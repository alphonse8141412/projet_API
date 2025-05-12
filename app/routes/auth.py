from flask import Blueprint, request, jsonify, g
from werkzeug.security import generate_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json

    # Vérifier que les champs nécessaires sont présents
    username = data.get('nom_user')
    password = data.get('motpasse')
    role = data.get('role', 'utilisateur')  # rôle par défaut

    if not username or not password:
        return jsonify({"error": "nom_user et motpasse sont requis"}), 400

    # Hacher le mot de passe pour la sécurité
    hashed_password = generate_password_hash(password)

    # Insérer l'utilisateur dans la base de données
    cur = g.db_conn.cursor()
    try:
        cur.execute(
            "INSERT INTO client (nom_user, motpasse, role) VALUES (%s, %s, %s);",
            (username, hashed_password, role)
        )
        g.db_conn.commit()
    except Exception as e:
        g.db_conn.rollback()
        return jsonify({"error": f"Erreur base de données : {str(e)}"}), 400
    finally:
        cur.close()

    return jsonify({"message": "Utilisateur créé avec succès"}), 201
