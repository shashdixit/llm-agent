import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# API Configuration
API_HOST = "127.0.0.1" 
API_PORT = 8009

# LLM Configuration
AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")
if not AIPROXY_TOKEN:
    raise ValueError("AIPROXY_TOKEN environment variable is not set")
    
LLM_API_URL = "https://aiproxy.sanand.workers.dev/openai/v1/embeddings"

# File System
DATA_DIR = Path("./data")  # Make this relative for testing

# Security
ALLOWED_PATHS = [DATA_DIR]