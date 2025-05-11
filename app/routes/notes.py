from flask import Blueprint, request, jsonify, g

notes_bp = Blueprint('notes', __name__)

# Lire toutes les notes
@notes_bp.route('/notes', methods=['GET'])
def get_notes():
    cur = g.db_conn.cursor()
    cur.execute("SELECT id_note, id_user, id_prompt, note FROM notes;")
    notes = cur.fetchall()
    cur.close()
    notes_list = [
        {'id_note': n[0], 'id_user': n[1], 'id_prompt': n[2], 'note': n[3]}
        for n in notes
    ]
    return jsonify(notes_list)

# Lire une note par id
@notes_bp.route('/notes/<int:id_note>', methods=['GET'])
def get_note(id_note):
    cur = g.db_conn.cursor()
    cur.execute("SELECT id_note, id_user, id_prompt, note FROM notes WHERE id_note = %s;", (id_note,))
    note = cur.fetchone()
    cur.close()
    if note:
        return jsonify({'id_note': note[0], 'id_user': note[1], 'id_prompt': note[2], 'note': note[3]})
    else:
        return jsonify({'error': 'Note non trouvée'}), 404

# Créer une note
@notes_bp.route('/notes', methods=['POST'])
def add_note():
    data = request.json
    required_fields = ['id_user', 'id_prompt', 'note']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Champs manquants'}), 400
    if not (1 <= data['note'] <= 5):
        return jsonify({'error': 'Note invalide, doit être entre 1 et 5'}), 400
    cur = g.db_conn.cursor()
    try:
        cur.execute(
            "INSERT INTO notes (id_user, id_prompt, note) VALUES (%s, %s, %s) RETURNING id_note;",
            (data['id_user'], data['id_prompt'], data['note'])
        )
        new_id = cur.fetchone()[0]
        g.db_conn.commit()
    except Exception as e:
        g.db_conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cur.close()
    return jsonify({'id_note': new_id}), 201

# Mettre à jour une note
@notes_bp.route('/notes/<int:id_note>', methods=['PUT'])
def update_note(id_note):
    data = request.json
    fields = ['id_user', 'id_prompt', 'note']
    set_clause = ", ".join(f"{field} = %s" for field in fields if field in data)
    if not set_clause:
        return jsonify({'error': 'Aucun champ à mettre à jour'}), 400
    if 'note' in data and not (1 <= data['note'] <= 5):
        return jsonify({'error': 'Note invalide, doit être entre 1 et 5'}), 400
    values = [data[field] for field in fields if field in data]
    values.append(id_note)
    cur = g.db_conn.cursor()
    cur.execute(f"UPDATE notes SET {set_clause} WHERE id_note = %s;", values)
    g.db_conn.commit()
    cur.close()
    return jsonify({'message': 'Note mise à jour'})

# Supprimer une note
@notes_bp.route('/notes/<int:id_note>', methods=['DELETE'])
def delete_note(id_note):
    cur = g.db_conn.cursor()
    cur.execute("DELETE FROM notes WHERE id_note = %s;", (id_note,))
    g.db_conn.commit()
    cur.close()
    return jsonify({'message': 'Note supprimée'})
