# Use the official Python image as base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install the dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container
COPY . .

# Expose port 8080 for the Flask app to listen on
EXPOSE 8080

# Set the environment variables for Redis host and port
ENV REDIS_HOST redis
ENV REDIS_PORT 6060

# Start the Flask app
CMD ["python", "app.py"]