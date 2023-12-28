# Use an official Python runtime as a parent image
FROM python:3.9.11

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip install requests pandas sqlalchemy
RUN pip install mysql-connector-python
RUN pip install plotly Flask

# Copy the current directory contents into the container at /app
COPY . /app

# Expose the port on which Flask will run
EXPOSE 5000

# Run the Flask app when the container launches
CMD ["python", "elastic.py"]
