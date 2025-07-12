# Use a slim Python base image
FROM python:3.11-slim

# Install MySQL client for `mysqldump` and cleanup cache to reduce image size
RUN apt-get update && \
    apt-get install -y default-mysql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory inside the container
WORKDIR /app

# Copy project files into container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the backup script
CMD ["python", "backup.py"]