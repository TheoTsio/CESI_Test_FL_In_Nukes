
# Use a lightweight official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies needed for compiling/running CatBoost
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install the exact required Python framework versions explicitly
RUN pip install --no-cache-dir \
    flwr==1.15.0 \
    catboost==1.2.10 \
    scikit-learn==1.5.2 \
    click==8.1.7 \
    torch==2.4.1 \
    torchvision==0.19.1

# Copy your local application scripts into the container
COPY task.py server_app.py client_app.py ./

# Expose Flower's communication ports
# 9091: ServerApp <-> SuperLink internal channel
# 9092: SuperNode <-> SuperLink external network channel
EXPOSE 9091 9092

# Ensure Python can see the modules in the current directory
ENV PYTHONPATH=/app