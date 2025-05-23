import psycopg2
from werkzeug.security import generate_password_hash

# Configuration de la base de données
DB_CONFIG = {
    "host":"localhost",
    "database":"robit_system",
    "user":"postgres",
    "password":"964Cfxgr@",
}

# Création de l'admin
admin_nom= "Coach"
admin_motpasse = generate_password_hash("mbengue866") 
admin_role = "Admin"

conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

try:
    cur.execute(
        "INSERT INTO client (nom_user, motpasse, role) VALUES (%s, %s, %s)",
        (admin_nom, admin_motpasse, admin_role)
    )
    conn.commit()
    print("Admin créé avec succès !")
except Exception as e:
    print("Erreur :", e)
    conn.rollback()
finally:
    cur.close()
    conn.close()
