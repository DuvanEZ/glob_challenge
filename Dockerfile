FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host=pypi.python.org --trusted-host=files.pythonhosted.org -r requirements.txt

# Copy all application files
COPY . .

# Expose the default port for Cloud Run
EXPOSE 8080

# Use Python to run your FastAPI app
CMD ["python", "-m", "src.app.main"]
