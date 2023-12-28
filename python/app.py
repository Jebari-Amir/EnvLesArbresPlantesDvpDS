from flask import Flask, render_template
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import sqlite3
import pandas as pd

app = Flask(__name__)

def generate_plot():
    # Connexion à la base de données SQLite
    conn = sqlite3.connect('ma_base_de_donnees.db')

    # Exécuter une requête pour récupérer les données
    select_query = "SELECT * FROM ArbresRemarquables;"
    cursor = conn.cursor()
    cursor.execute(select_query)

    # Lire les données directement dans un DataFrame
    df = pd.read_sql_query(select_query, conn)

    # Fermer la connexion
    conn.close()

    # Générer le graphique
    plt.scatter(df['geom_lon'], df['geom_lat'])
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Corrélation entre geom_lon et geom_lat')

    # Convertir le graphique en image
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    plt.close()

    # Convertir l'image en base64 pour l'intégrer dans la page HTML
    encoded_image = base64.b64encode(image_stream.read()).decode('utf-8')

    return encoded_image

@app.route('/')
def index():
    # Générer le graphique
    plot_data = generate_plot()

    # Passer les données à la page HTML
    return render_template('visualisation.html', plot_data=plot_data)

if __name__ == '__main__':
    app.run(debug=True)
