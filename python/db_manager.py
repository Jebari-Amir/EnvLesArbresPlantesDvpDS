import mysql.connector

def connect_to_database():
    # Remplacez ces valeurs par les informations de votre base de données
    config = {
        'user': 'root',
        'password': '',
        'host': '3306',
        'database': 'thequanticfactory',
        'raise_on_warnings': True
    }

    # Établir la connexion
    conn = mysql.connector.connect(**config)
    return conn

def fetch_data(conn):
    # Créer un curseur
    cursor = conn.cursor()

    # Exemple de requête SELECT
    cursor.execute("SELECT * FROM thequanticfactory")
    result = cursor.fetchall()

    # Fermer le curseur
    cursor.close()

    return result
