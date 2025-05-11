from flask import Blueprint, request, jsonify, g

prompt_bp = Blueprint('prompt', __name__)

# Lire tous les prompts
@prompt_bp.route('/prompts', methods=['GET'])
def get_prompts():
    cur = g.db_conn.cursor()
    cur.execute("""
        SELECT id_prompt, nom, description, id_client, prix, statut 
        FROM prompt;
    """)
    prompts = cur.fetchall()
    cur.close()
    prompts_list = [
        {
            'id_prompt': p[0],
            'nom': p[1],
            'description': p[2],
            'id_client': p[3],
            'prix': float(p[4]),
            'statut': p[5]
        }
        for p in prompts
    ]
    return jsonify(prompts_list)

# Lire un prompt par id
@prompt_bp.route('/prompts/<int:id_prompt>', methods=['GET'])
def get_prompt(id_prompt):
    cur = g.db_conn.cursor()
    cur.execute("""
        SELECT id_prompt, nom, description, id_client, prix, statut 
        FROM prompt WHERE id_prompt = %s;
    """, (id_prompt,))
    p = cur.fetchone()
    cur.close()
    if p:
        prompt = {
            'id_prompt': p[0],
            'nom': p[1],
            'description': p[2],
            'id_client': p[3],
            'prix': float(p[4]),
            'statut': p[5]
        }
        return jsonify(prompt)
    else:
        return jsonify({'error': 'Prompt non trouvé'}), 404

# Créer un nouveau prompt
@prompt_bp.route('/prompts', methods=['POST'])
def add_prompt():
    data = request.json
    required_fields = ['nom', 'description', 'id_client', 'prix']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Champs manquants'}), 400

    statut = data.get('statut', 'en_attente')  # statut par défaut

    cur = g.db_conn.cursor()
    cur.execute("""
        INSERT INTO prompt (nom, description, id_client, prix, statut)
        VALUES (%s, %s, %s, %s, %s) RETURNING id_prompt;
    """, (data['nom'], data['description'], data['id_client'], data['prix'], statut))
    new_id = cur.fetchone()[0]
    g.db_conn.commit()
    cur.close()
    return jsonify({'id_prompt': new_id}), 201

# Mettre à jour un prompt
@prompt_bp.route('/prompts/<int:id_prompt>', methods=['PUT'])
def update_prompt(id_prompt):
    data = request.json
    fields = ['nom', 'description', 'id_client', 'prix', 'statut']
    set_clause = ", ".join(f"{field} = %s" for field in fields if field in data)
    if not set_clause:
        return jsonify({'error': 'Aucun champ à mettre à jour'}), 400

    values = [data[field] for field in fields if field in data]
    values.append(id_prompt)

    cur = g.db_conn.cursor()
    query = f"UPDATE prompt SET {set_clause} WHERE id_prompt = %s;"
    cur.execute(query, values)
    g.db_conn.commit()
    cur.close()
    return jsonify({'message': 'Prompt mis à jour'})

# Supprimer un prompt
@prompt_bp.route('/prompts/<int:id_prompt>', methods=['DELETE'])
def delete_prompt(id_prompt):
    cur = g.db_conn.cursor()
    cur.execute("DELETE FROM prompt WHERE id_prompt = %s;", (id_prompt,))
    g.db_conn.commit()
    cur.close()
    return jsonify({'message': 'Prompt supprimé'})
