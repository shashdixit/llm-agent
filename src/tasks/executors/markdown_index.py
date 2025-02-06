import json
from pathlib import Path
from ...utils.file_ops import FileOps

class MarkdownIndexExecutor:
    def __init__(self):
        self.file_ops = FileOps()

    async def execute(self, parameters: dict) -> bool:
        try:
            # Get all markdown files in /data/docs/
            docs_dir = Path("data/docs")
            markdown_files = await self.file_ops.list_files(str(docs_dir), "**/*.md")
            
            index = {}
            for file_path in markdown_files:
                # Read the file content
                content = await self.file_ops.read_file(str(file_path))
                
                # Find first H1 heading
                for line in content.split('\n'):
                    if line.strip().startswith('# '):
                        # Remove the '# ' and any trailing whitespace
                        title = line.strip()[2:].strip()
                        # Get relative path from /data/docs/
                        relative_path = str(file_path.relative_to(docs_dir))
                        index[relative_path] = title
                        break
                        
            # Write the index to JSON file
            output_path = "data/docs/index.json"
            await self.file_ops.write_file(
                output_path, 
                json.dumps(index, indent=2)
            )
            return True
            
        except Exception as e:
            raise Exception(f"Failed to create markdown index: {str(e)}")