import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# API Configuration
API_HOST = "127.0.0.1"  # Changed to allow external access
API_PORT = 8009  # Standard HTTPS port

# SSL Configuration (for development)
SSL_ENABLED = True
SSL_KEYFILE = os.path.join(os.path.dirname(__file__), "..", "key.pem")
SSL_CERTFILE = os.path.join(os.path.dirname(__file__), "..", "cert.pem")

# LLM Configuration
AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")
if not AIPROXY_TOKEN:
    raise ValueError("AIPROXY_TOKEN environment variable is not set")

# File System
DATA_DIR = Path("./data")