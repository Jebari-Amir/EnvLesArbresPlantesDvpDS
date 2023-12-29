import requests
import pandas as pd
from time import sleep
import mysql.connector
from sqlalchemy import create_engine
import plotly.graph_objects as go
import plotly.express as px
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Make a request to the API
    api_url = "https://opendata.paris.fr/api/explore/v2.1"
    dataset_endpoint = "/catalog/datasets/les-arbres-plantes/exports/csv"
    response = requests.get(api_url + dataset_endpoint)

    # Ensure the response content is in UTF-8 encoding and ignore BOM
    response.encoding = 'utf-8-sig'

    # Check if the response is successful (status code 200)
    if response.status_code == 200:
        # Save the CSV content to a file
        with open("output.csv", "wb") as csv_file:
            csv_file.write(response.content)
        print("CSV file downloaded successfully.")

        # Read CSV into pandas DataFrame
        df = pd.read_csv("output.csv", sep=';', on_bad_lines='skip')

        # Modify the original DataFrame in place
        df.dropna(inplace=True)
        df.drop_duplicates(inplace=True)

        # Wait for MySQL to become available
        sleep(2)  # Adjust the sleep duration based on your system's performance and MySQL startup time

        # Replace 'your_username' and 'your_password' with your MySQL credentials
        username = 'root'
        password = 'pass'

        # Specify the MySQL host, port, database name, and authentication details
        mysql_host = 'mysql1'  # Update with the service name from Docker Compose
        mysql_port = 3306
        mysql_db_name = 'test'  # Specify your MySQL database name
        my = 'my'  # Specify your MySQL table name

        # Create a MySQL connection using MySQL Connector
        try:
            connection = mysql.connector.connect(
                host=mysql_host,
                port=mysql_port,
                user=username,
                password=password,
                database=mysql_db_name
            )
            print("Connected to MySQL.")

            # Use SQLAlchemy to create a custom engine for MySQL
            engine = create_engine(
                f"mysql+mysqlconnector://{username}:{password}@{mysql_host}:{mysql_port}/{mysql_db_name}")

            # Drop the existing table if it exists
            connection.cursor().execute(f"DROP TABLE IF EXISTS {my}")

            # Create the table using pandas to_sql with the custom engine
            df.to_sql(name=my, con=engine, if_exists='replace', index=False)

            print("Data inserted into MySQL.")

        except Exception as e:
            print(f"Error interacting with MySQL. Error: {str(e)}")
        finally:
            # Close the connection
            if 'connection' in locals() and connection is not None:
                connection.close()

        # Count the occurrences of each unique value in the 'espece' column
        species_counts = df['espece'].value_counts().reset_index()
        species_counts.columns = ['Species', 'Count']

        # Create a bar chart using Plotly graph objects
        bar_chart = px.bar(species_counts, x='Species', y='Count', title='Number of Trees by Species',
                           labels={'Count': 'Number of Trees', 'Species': 'Tree Species'},
                           color='Count', color_continuous_scale='Viridis')

        pie_chart = px.pie(species_counts, names='Species', values='Count', title='Distribution of Tree Species',
                           labels={'Species': 'Number of Trees'},
                           hole=0.3)

        # Create a scatter plot using Plotly graph objects
        scatter_plot = px.scatter(df, x='geo_shape', y='geo_point_2d', color='espece', title='Tree Locations',
                                  labels={'geo_shape': 'Longitude', 'geo_point_2d': 'Latitude'},
                                  size_max=10, opacity=0.6)
        selected_columns = ['circonferenceencm', 'hauteurenm']

        # Drop non-numeric columns before calculating the correlation matrix
        numeric_columns = df[selected_columns].select_dtypes(include=['float64', 'int64']).columns
        corr_matrix = df[numeric_columns].corr()

        # Convert Plotly charts to div elements containing JavaScript code
        bar_chart_div = px.bar(species_counts, x='Species', y='Count', title='Number of Trees by Species',
                               labels={'Count': 'Number of Trees', 'Species': 'Tree Species'},
                               color='Count', color_continuous_scale='Viridis').to_html(full_html=False)

        pie_chart_div = px.pie(species_counts, names='Species', values='Count',
                               title='Distribution of Tree Species').to_html(full_html=False)

        scatter_plot_div = px.scatter(df, x='geo_shape', y='geo_point_2d', color='espece', title='Tree Locations',
                                      labels={'geo_shape': 'Longitude', 'geo_point_2d': 'Latitude'},
                                      size_max=10, opacity=0.6).to_html(full_html=False)

        corr_matrix_div = go.Figure(data=go.Heatmap(z=corr_matrix.values,
                                                    x=corr_matrix.columns,
                                                    y=corr_matrix.columns)).to_html(full_html=False)

        return render_template('visualisation.html', bar_chart_div=bar_chart_div, pie_chart_div=pie_chart_div,
                               scatter_plot_div=scatter_plot_div, corr_matrix_div=corr_matrix_div)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
