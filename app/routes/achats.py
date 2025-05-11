from flask import Blueprint, request, jsonify, g

achats_bp = Blueprint('achats', __name__)

# Lire tous les achats
@achats_bp.route('/achats', methods=['GET'])
def get_achats():
    cur = g.db_conn.cursor()
    cur.execute("SELECT id_achat, id_prompt, prix FROM achats;")
    achats = cur.fetchall()
    cur.close()
    achats_list = [
        {'id_achat': a[0], 'id_prompt': a[1], 'prix': float(a[2])}
        for a in achats
    ]
    return jsonify(achats_list)

# Lire un achat par id
@achats_bp.route('/achats/<int:id_achat>', methods=['GET'])
def get_achat(id_achat):
    cur = g.db_conn.cursor()
    cur.execute("SELECT id_achat, id_prompt, prix FROM achats WHERE id_achat = %s;", (id_achat,))
    achat = cur.fetchone()
    cur.close()
    if achat:
        return jsonify({'id_achat': achat[0], 'id_prompt': achat[1], 'prix': float(achat[2])})
    else:
        return jsonify({'error': 'Achat non trouvé'}), 404

# Créer un achat
@achats_bp.route('/achats', methods=['POST'])
def add_achat():
    data = request.json
    required_fields = ['id_prompt', 'prix']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Champs manquants'}), 400
    cur = g.db_conn.cursor()
    cur.execute(
        "INSERT INTO achats (id_prompt, prix) VALUES (%s, %s) RETURNING id_achat;",
        (data['id_prompt'], data['prix'])
    )
    new_id = cur.fetchone()[0]
    g.db_conn.commit()
    cur.close()
    return jsonify({'id_achat': new_id}), 201

# Mettre à jour un achat
@achats_bp.route('/achats/<int:id_achat>', methods=['PUT'])
def update_achat(id_achat):
    data = request.json
    fields = ['id_prompt', 'prix']
    set_clause = ", ".join(f"{field} = %s" for field in fields if field in data)
    if not set_clause:
        return jsonify({'error': 'Aucun champ à mettre à jour'}), 400
    values = [data[field] for field in fields if field in data]
    values.append(id_achat)
    cur = g.db_conn.cursor()
    query = f"UPDATE achats SET {set_clause} WHERE id_achat = %s;"
    cur.execute(query, values)
    g.db_conn.commit()
    cur.close()
    return jsonify({'message': 'Achat mis à jour'})

# Supprimer un achat
@achats_bp.route('/achats/<int:id_achat>', methods=['DELETE'])
def delete_achat(id_achat):
    cur = g.db_conn.cursor()
    cur.execute("DELETE FROM achats WHERE id_achat = %s;", (id_achat,))
    g.db_conn.commit()
    cur.close()
    return jsonify({'message': 'Achat supprimé'})
