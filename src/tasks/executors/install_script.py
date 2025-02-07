import os
import subprocess
import sys
import httpx
from ...utils.logger import logger

class InstallScriptExecutor:
    async def execute(self, params: dict) -> bool:
        try:
            # Get the current working directory (root of the project)
            root_dir = os.getcwd()
            data_dir = os.path.join(root_dir, 'data')
            os.makedirs(data_dir, exist_ok=True)

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
            email = params.get('email', 'shashwat.dixit@gramener.com')

            if not email:
                raise ValueError("Email parameter is required")

            script_path = os.path.join(data_dir, 'datagen.py')
            
            # Download script
            async with httpx.AsyncClient() as client:
                response = await client.get(script_url)
                if response.status_code != 200:
                    raise Exception(f"Failed to download script: {response.status_code}")
                
                with open(script_path, 'wb') as f:
                    f.write(response.content)

            # Make script executable
            os.chmod(script_path, 0o755)

            # Update parameters to use relative paths
            input_dir = os.path.join(root_dir, 'data', 'docs')
            output_file = os.path.join(root_dir, 'data', 'docs', 'index.json')
            params['input_dir'] = input_dir
            params['output_file'] = output_file

            # Run script with root_dir argument
            try:
                result = subprocess.run(
                    [sys.executable, script_path, email, '--root', data_dir],
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
