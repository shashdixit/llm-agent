# run.py (in root directory)
import uvicorn
from src.config import (
    API_HOST, 
    API_PORT, 
    SSL_ENABLED, 
    SSL_KEYFILE, 
    SSL_CERTFILE
)

if __name__ == "__main__":
    config = {
        "app": "src.main:app",
        "host": API_HOST,
        "port": API_PORT,
        "reload": True,
    }
    
    if SSL_ENABLED:
        config.update({
            "ssl_keyfile": SSL_KEYFILE,
            "ssl_certfile": SSL_CERTFILE
        })
    
    uvicorn.run(**config)