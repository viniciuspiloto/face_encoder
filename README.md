# Face Encoder Project

## Overview
The Face Encoder project is a FastAPI-based service that allows users to upload images for face encoding. It provides functionalities for starting a new session, uploading images, and retrieving session summaries.

## Prerequisites
- Python 3.6 or higher
- Docker
- Docker Compose

## Installation
1. Clone the repository
2. Set up the environment variables in a `.env` file. You can use the `env.template` file
3. Build the Docker containers with `docker compose build`
4. Start Docker containers with `docker compose up`

> If you want to test the application on your own, you can use the DockerHub image [vpilotoamaro/face-encoder:latest](https://hub.docker.com/r/vpilotoamaro/face-encoder/tags)

## Test
You can test the application with Swagger by openning http://localhost:8001/docs

## Features
- **Start Session:** Start a new session for face encoding
- **Upload Image:** Upload an image for face encoding
- **Session Summary:** Retrieve a summary of the session

## Endpoints
- **/start_session:** POST method to start a new session
- **/upload:** POST method to upload an image
- **/session_summary/{session_id}:** GET method to get the session summary

## Next Steps
- Add queueing service for uploading images for better performance and scalability. (RabbitMQ with Celery)
- Session caching for better performance. (Redis)

## Contributors
- Vinicius Amaro <vpilotoamaro@gmail.com>
