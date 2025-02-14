# run.py (in root directory)
import uvicorn
from src.config import (
    API_HOST, 
    API_PORT
)

if __name__ == "__main__":
    config = {
        "app": "src.main:app",
        "host": API_HOST,
        "port": API_PORT,
        "reload": True,
    }
    
    uvicorn.run(**config)