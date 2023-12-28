from elasticsearch import Elasticsearch

import os
from elasticsearch import Elasticsearch

# Use environment variables for Elasticsearch credentials
username = os.getenv('ELASTICSEARCH_USERNAME')
password = os.getenv('ELASTICSEARCH_PASSWORD')

# Specify the Elasticsearch host, port, and authentication details
c = Elasticsearch(
    [{'host': 'localhost', 'port': 9200, 'scheme': 'http'}],
    http_auth=(username, password),
    request_timeout=60
)

if c.ping():
    print("Connected to Elasticsearch.")
    print(c.ping())
else:
    print("Unable to connect to Elasticsearch.")