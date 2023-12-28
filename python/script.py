# Importez votre module de gestion de la base de données
from db_manager import connect_to_database, fetch_data

# Établissez la connexion à la base de données
conn = connect_to_database()

# Utilisez votre module de gestion de la base de données pour récupérer des données
data = fetch_data(conn)

# Faites quelque chose avec les données, par exemple, imprimez-les
for row in data:
    print(row)

# Fermez la connexion à la base de données
conn.close()
