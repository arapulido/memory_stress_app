# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the application files
COPY memory_stress.py /app/
COPY requirements.txt /app/

# Make the script executable
RUN chmod +x /app/memory_stress.py

# Set the entrypoint
ENTRYPOINT ["python", "/app/memory_stress.py"]