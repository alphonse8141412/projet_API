from flask import Blueprint, request, jsonify, g
from app.decorators import role_required


votes_bp = Blueprint('votes', __name__)
prompt_bp = Blueprint('prompt', __name__)




# Lire tous les votes
@votes_bp.route('/votes', methods=['GET'])
@role_required("utilisateur")
def get_votes():
    cur = g.db_conn.cursor()
    cur.execute("SELECT id_vote, id_user, id_prompt, vote FROM votes;")
    votes = cur.fetchall()
    cur.close()
    votes_list = [
        {'id_vote': v[0], 'id_user': v[1], 'id_prompt': v[2], 'vote': v[3]}
        for v in votes
    ]
    return jsonify(votes_list)

# Lire un vote par id
@votes_bp.route('/votes/<int:id_vote>', methods=['GET'])
@role_required("utilisateur")
def get_vote(id_vote):
    cur = g.db_conn.cursor()
    cur.execute("SELECT id_vote, id_user, id_prompt, vote FROM votes WHERE id_vote = %s;", (id_vote,))
    vote = cur.fetchone()
    cur.close()
    if vote:
        return jsonify({'id_vote': vote[0], 'id_user': vote[1], 'id_prompt': vote[2], 'vote': vote[3]})
    else:
        return jsonify({'error': 'Vote non trouvé'}), 404

# Créer un vote
@votes_bp.route('/votes', methods=['POST'])
@role_required("utilisateur")
def add_vote():
    data = request.json
    required_fields = ['id_user', 'id_prompt', 'vote']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Champs manquants'}), 400
    if data['vote'] not in [0, 1]:
        return jsonify({'error': 'Valeur de vote invalide'}), 400
    cur = g.db_conn.cursor()
    try:
        cur.execute(
            "INSERT INTO votes (id_user, id_prompt, vote) VALUES (%s, %s, %s) RETURNING id_vote;",
            (data['id_user'], data['id_prompt'], data['vote'])
        )
        new_id = cur.fetchone()[0]
        g.db_conn.commit()
    except Exception as e:
        g.db_conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cur.close()
    return jsonify({'id_vote': new_id}), 201

# Mettre à jour un vote
@votes_bp.route('/votes/<int:id_vote>', methods=['PUT'])
@role_required("utilisateur")
def update_vote(id_vote):
    data = request.json
    fields = ['id_user', 'id_prompt', 'vote']
    set_clause = ", ".join(f"{field} = %s" for field in fields if field in data)
    if not set_clause:
        return jsonify({'error': 'Aucun champ à mettre à jour'}), 400
    if 'vote' in data and data['vote'] not in [0, 1]:
        return jsonify({'error': 'Valeur de vote invalide'}), 400
    values = [data[field] for field in fields if field in data]
    values.append(id_vote)
    cur = g.db_conn.cursor()
    cur.execute(f"UPDATE votes SET {set_clause} WHERE id_vote = %s;", values)
    g.db_conn.commit()
    cur.close()
    return jsonify({'message': 'Vote mis à jour'})

# Supprimer un vote
@votes_bp.route('/votes/<int:id_vote>', methods=['DELETE'])
@role_required("utilisateur")
def delete_vote(id_vote):
    cur = g.db_conn.cursor()
    cur.execute("DELETE FROM votes WHERE id_vote = %s;", (id_vote,))
    g.db_conn.commit()
    cur.close()
    return jsonify({'message': 'Vote supprimé'})
