# src/tasks/executors/install_script.py

import os
import subprocess
import sys
import httpx
from ...utils.logger import logger

class InstallScriptExecutor:
    async def execute(self, params: dict) -> bool:
        try:
            # Ensure data directory exists
            os.makedirs('data', exist_ok=True)

            # Install uv if not present
            try:
                subprocess.run(['uv', '--version'], check=True, capture_output=True)
                logger.info("uv is already installed")
            except (subprocess.CalledProcessError, FileNotFoundError):
                logger.info("Installing uv...")
                subprocess.run([
                    sys.executable, 
                    '-m', 
                    'pip', 
                    'install', 
                    'uv'
                ], check=True)

            # Download and run script
            script_url = params['script_url']
            email = params.get('email', os.getenv('USER_EMAIL'))

            if not email:
                raise ValueError("Email parameter is required")

            script_path = os.path.join('data', 'datagen.py')
            
            # Download script
            async with httpx.AsyncClient() as client:
                response = await client.get(script_url)
                if response.status_code != 200:
                    raise Exception(f"Failed to download script: {response.status_code}")
                
                with open(script_path, 'wb') as f:  # Changed to 'wb' mode
                    f.write(response.content)  # Use content instead of text

            # Make script executable
            os.chmod(script_path, 0o755)

            # Run script with more detailed error handling
            try:
                result = subprocess.run(
                    [sys.executable, script_path, email],
                    check=True,
                    capture_output=True,
                    text=True
                )
                logger.info(f"Script output: {result.stdout}")
            except subprocess.CalledProcessError as e:
                logger.error(f"Script execution failed. Exit code: {e.returncode}")
                logger.error(f"stdout: {e.stdout}")
                logger.error(f"stderr: {e.stderr}")
                raise

            return True

        except Exception as e:
            logger.error(f"Error in InstallScriptExecutor: {str(e)}")
            raise