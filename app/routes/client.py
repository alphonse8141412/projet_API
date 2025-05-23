from flask import Blueprint, request, jsonify, g
from app.decorators import role_required
from flask_jwt_extended import jwt_required, get_jwt_identity


client_bp = Blueprint('client', __name__)


#décorateur
some_bp = Blueprint('some', __name__)


 
# Lire tous les clients
@client_bp.route('/clients', methods=['GET'])
@role_required("Admin")
def get_clients():
    cur = g.db_conn.cursor()
    cur.execute("SELECT id_client, nom_user, id_groupe, role FROM client;")
    clients = cur.fetchall()
    cur.close()
    clients_list = [
        {'id_client': c[0], 'nom_user': c[1], 'id_groupe': c[2], 'role': c[3]}
        for c in clients
    ]
    return jsonify(clients_list)

# Lire un client par id
@client_bp.route('/clients/<int:id_client>', methods=['GET'])
@role_required("Admin")
def get_client(id_client):
    cur = g.db_conn.cursor()
    cur.execute("SELECT id_client, nom_user, id_groupe, role FROM client WHERE id_client = %s;", (id_client,))
    client = cur.fetchone()
    cur.close()
    if client:
        return jsonify({'id_client': client[0], 'nom_user': client[1], 'id_groupe': client[2], 'role': client[3]})
    else:
        return jsonify({'error': 'Client non trouvé'}), 404

# Créer un nouveau client


# Mettre à jour un client
@client_bp.route('/clients/<int:id_client>', methods=['PUT'])
@role_required("Admin")
def update_client(id_client):
    data = request.json
    cur = g.db_conn.cursor()
    cur.execute(
        "UPDATE client SET nom_user=%s, motpasse=%s, id_groupe=%s, role=%s WHERE id_client=%s;",
        (data['nom_user'], data['motpasse'], data['id_groupe'], data['role'], id_client)
    )
    g.db_conn.commit()
    cur.close()
    return jsonify({'message': 'Client mis à jour'})

# Supprimer un client
@client_bp.route('/clients/<int:id_client>', methods=['DELETE'])
@role_required("Admin")
def delete_client(id_client):
    cur = g.db_conn.cursor()
    cur.execute("DELETE FROM client WHERE id_client=%s;", (id_client,))
    g.db_conn.commit()
    cur.close()
    return jsonify({'message': 'Client supprimé'})
