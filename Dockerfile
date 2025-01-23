FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Expose the default port for Cloud Run (optional)
EXPOSE 8080

# Use Python to run your FastAPI app
CMD ["python", "-m", "src.app.main"]
