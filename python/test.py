import matplotlib.pyplot as plt
import sqlite3
import pandas as pd

# Connexion à la base de données SQLite
conn = sqlite3.connect('ma_base_de_donnees.db')
cursor = conn.cursor()

# Exécuter une requête pour récupérer les données
select_query = "SELECT * FROM ArbresRemarquables;"
cursor.execute(select_query)

# Lire les données directement dans un DataFrame
df = pd.read_sql_query(select_query, conn)

# Fermer la connexion
conn.close()

print("****success***")


print("//////////////////////////////////////////////////////////////////")
# Afficher les premières lignes du DataFrame pour inspecter les données
print(df.head())

# Calculer la corrélation entre geom_lon et geom_lat
correlation_lon_lat = df['geom_lon'].corr(df['geom_lat'])
print(f"Corrélation entre geom_lon et geom_lat : {correlation_lon_lat}")

# Créer un graphique pour visualiser la corrélation
plt.scatter(df['geom_lon'], df['geom_lat'])
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Corrélation entre geom_lon et geom_lat')
plt.show()







