# Task Manager Application

A multi-container application consisting of a Flask web application and a MongoDB database, deployed with Docker and Kubernetes.

## Project Overview

This project implements a simple Task Manager application with the following features:
- View a list of tasks
- Add new tasks
- Mark tasks as complete
- Delete tasks

The application is containerized using Docker, with a CI/CD pipeline implemented using GitHub Actions, and deployed on Kubernetes using Minikube.

## Project Structure

task-manager/
├── app/                      # Flask application
│   ├── templates/            # HTML templates
│   ├── app.py                # Main application file
│   ├── models.py             # Database models
│   ├── routes.py             # Application routes
│   ├── __init__.py           # Application initialization
│   ├── requirements.txt      # Python dependencies
│   ├── Dockerfile            # Docker configuration for Flask app
│   └── docker-compose.yml    # Docker Compose configuration
└── k8s-manifests/            # Kubernetes manifests
    ├── flask-deployment.yaml # Flask application deployment
    ├── flask-service.yaml    # Flask application service
    ├── mongodb-deployment.yaml # MongoDB deployment
    ├── mongodb-service.yaml  # MongoDB service
    ├── configmap.yaml        # ConfigMap for non-sensitive data
    └── secret.yaml           # Secret for sensitive data

## Prerequisites

- Docker
- Kubernetes (Minikube)
- kubectl
- Python 3.9+
- Git

## Local Development

### Setup

1. Clone the repository:
   git clone https://github.com/yourusername/task-manager.git
   cd task-manager

2. Create and activate a virtual environment:
   python -m venv venv
   venv\Scripts\activate

3. Install dependencies:
   cd app
   pip install -r requirements.txt

4. Set up environment variables:
   Create a .env file in the app directory with the following variables:
   MONGO_INITDB_ROOT_USERNAME=admin
   MONGO_INITDB_ROOT_PASSWORD=password
   FLASK_SECRET_KEY=dev-secret-key

### Running with Docker Compose

1. Build and start the containers:
   cd app
   docker-compose up --build

2. Access the application at http://localhost:5000

### Running with Kubernetes (Minikube)

1. Start Minikube:
   minikube start

2. Apply Kubernetes manifests:
   kubectl apply -f k8s-manifests/

3. Create the necessary secrets:
   kubectl create secret generic app-secrets \
     --from-literal=flask-secret-key=your-flask-secret \
     --from-literal=mongo-username=your-mongo-username \
     --from-literal=mongo-password=your-mongo-password

4. Access the application:
   minikube service flask-app

## CI/CD Pipeline

The project includes a GitHub Actions workflow for continuous integration and deployment:

- Continuous Integration: Triggered on pushes to the dev branch
  - Performs Python code linting
  - Builds the Docker image to confirm successful builds

- Continuous Deployment: Triggered when PRs are merged to the main branch
  - Builds and tags the Docker image
  - Pushes the Docker image to Docker Hub
  - Updates Kubernetes deployment manifest files with the new Docker image tag
  - Updates the Kubernetes cluster with the new deployment

## Configuration Management

- ConfigMap: Stores non-sensitive configuration data
  - MongoDB connection information (host, port, database name)
  - Debug mode setting

- Secrets: Stores sensitive information
  - Flask Secret Key
  - MongoDB username and password

## Troubleshooting

If you encounter issues with the application:

1. Check the logs of the Flask application:
   kubectl logs -l app=flask-app

2. Check the logs of the MongoDB instance:
   kubectl logs -l app=mongodb

3. Verify that the services are running:
   kubectl get services

4. Verify that the pods are running:
   kubectl get pods