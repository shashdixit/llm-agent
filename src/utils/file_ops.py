# src/utils/file_ops.py

from pathlib import Path
import aiofiles
import os

class FileOps:
    async def read_file(self, path: str) -> str:
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
            
        async with aiofiles.open(path, 'r') as f:
            return await f.read()
            
    async def write_file(self, path: str, content: str) -> None:
        # Ensure absolute path or use project root
        if not os.path.isabs(path):
            # Use project root directory
            project_root = Path(__file__).parent.parent.parent
            path = str(project_root / path)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        async with aiofiles.open(path, 'w') as f:
            await f.write(content)
            
    async def list_files(self, directory: str, pattern: str = "*") -> list:
        return list(Path(directory).glob(pattern))