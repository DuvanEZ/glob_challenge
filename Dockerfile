# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev

# Install FastAPI, Uvicorn, and any other needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run Uvicorn to serve the FastAPI app when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]