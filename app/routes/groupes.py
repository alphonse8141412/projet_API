from flask import Blueprint, request, jsonify, g
# from flask_jwt_extended import jwt_required
# from app.decorators import role_required



groupes_bp = Blueprint('groupes', __name__)



# # Créer un groupe d'utilisateurs
# @groupes_bp.route('/groupes', methods=['POST'])
# @jwt_required()
# @role_required('Admin')
# def create_group():
#     # Code pour créer un groupe
#     pass
# # Lire tous les groupes
@groupes_bp.route('/groupes', methods=['GET'])
def get_groupes():
    cur = g.db_conn.cursor()
    cur.execute("SELECT id_goupe, nom_groupe FROM groupes;")
    groupes = cur.fetchall()
    cur.close()
    groupes_list = [{'id_goupe': g[0], 'nom_groupe': g[1]} for g in groupes]
    return jsonify(groupes_list)

# Lire un groupe par id
@groupes_bp.route('/groupes/<int:id_goupe>', methods=['GET'])
def get_groupe(id_goupe):
    cur = g.db_conn.cursor()
    cur.execute("SELECT id_goupe, nom_groupe FROM groupes WHERE id_goupe = %s;", (id_goupe,))
    groupe = cur.fetchone()
    cur.close()
    if groupe:
        return jsonify({'id_goupe': groupe[0], 'nom_groupe': groupe[1]})
    else:
        return jsonify({'error': 'Groupe non trouvé'}), 404

# Créer un groupe
@groupes_bp.route('/groupes', methods=['POST'])
def add_groupe():
    data = request.json
    if 'nom_groupe' not in data:
        return jsonify({'error': 'nom_groupe manquant'}), 400
    cur = g.db_conn.cursor()
    cur.execute("INSERT INTO groupes (nom_groupe) VALUES (%s) RETURNING id_goupe;", (data['nom_groupe'],))
    new_id = cur.fetchone()[0]
    g.db_conn.commit()
    cur.close()
    return jsonify({'id_goupe': new_id}), 201

# Mettre à jour un groupe
@groupes_bp.route('/groupes/<int:id_goupe>', methods=['PUT'])
def update_groupe(id_goupe):
    data = request.json
    if 'nom_groupe' not in data:
        return jsonify({'error': 'nom_groupe manquant'}), 400
    cur = g.db_conn.cursor()
    cur.execute("UPDATE groupes SET nom_groupe=%s WHERE id_goupe=%s;", (data['nom_groupe'], id_goupe))
    g.db_conn.commit()
    cur.close()
    return jsonify({'message': 'Groupe mis à jour'})

# Supprimer un groupe
@groupes_bp.route('/groupes/<int:id_goupe>', methods=['DELETE'])
def delete_groupe(id_goupe):
    cur = g.db_conn.cursor()
    cur.execute("DELETE FROM groupes WHERE id_goupe=%s;", (id_goupe,))
    g.db_conn.commit()
    cur.close()
    return jsonify({'message': 'Groupe supprimé'})
