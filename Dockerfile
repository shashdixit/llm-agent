FROM python:3.9

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# Generate SSL certificates
RUN openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365 -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

# Expose the HTTPS port
EXPOSE 8000

# Command to run the application
CMD ["python", "run.py"]