# src/main.py

from fastapi import FastAPI, HTTPException, Query
from src.tasks.parser import TaskParser
from src.tasks.executor import TaskExecutor
from src.utils.security import SecurityCheck
from src.utils.file_ops import FileOps
import logging
import uvicorn
from .config import API_PORT, API_HOST

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
parser = TaskParser()
executor = TaskExecutor()
security = SecurityCheck()
file_ops = FileOps()

@app.post("/run")
async def run_task(task: str = Query(..., description="Task description")):
    try:
        # Parse task
        task_info = await parser.parse_task(task)
        logger.info(f"Parsed task info: {task_info}")
        
        # Execute task
        try:
            success = await executor.execute_task(task_info)
            
            if success:
                return {
                    "status": "success",
                    "message": "Task executed successfully",
                    "task_info": task_info
                }
        except Exception as e:
            logger.error(f"Task execution error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Task execution failed: {str(e)}"
            )
            
    except ValueError as e:
        logger.error(f"Bad request: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/read")
async def read_file(path: str = Query(..., description="File path to read")):
    try:
        # Remove any quotes and normalize path
        path = path.strip("'\"")
        
        # Normalize path to handle leading slashes
        if path.startswith('/'):
            path = path.lstrip('/')
        
        # Security check
        if not security.is_path_allowed(path):
            raise HTTPException(
                status_code=404, 
                detail="File not found or access denied"
            )
            
        try:
            content = await file_ops.read_file(path)
            return {"content": content}
        except FileNotFoundError:
            raise HTTPException(
                status_code=404, 
                detail="File not found"
            )
            
    except Exception as e:
        logger.error(f"Error reading file: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error reading file: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=API_HOST,
        port=API_PORT,
        reload=True
    )
