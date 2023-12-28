terraform {
  required_providers {
    docker = {
      source = "kreuzwerker/docker"
    }
  }
}

provider "docker" {
  host = "tcp://192.168.56.1:2375"
}

resource "docker_image" "elasticsearch" {
  name = "elasticsearch:7.18.1"  # Specify the desired version
}

resource "docker_container" "elasticsearch" {
  image = docker_image.elasticsearch.name
  name  = "elasticsearch"
  ports {
    internal = 9200
    external = 9200
  }
  volumes {
    host_path = "/path/to/elasticsearch/data"  # Replace with your data path
    container_path = "/usr/share/elasticsearch/data"
  }
  env = [
    "discovery.type=single-node",
    "ES_JAVA_OPTS=-Xms512m -Xmx512m"  # Adjust memory settings
  ]
}

resource "null_resource" "index_creation" {
  provisioner "local-exec" {
    command = "curl -X PUT http://localhost:9200/my-index -H 'Content-Type: application/json' -d @elasticsearch-template.json"
  }

  depends_on = [docker_container.elasticsearch]
}
