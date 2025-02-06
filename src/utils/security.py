from pathlib import Path
import os

class SecurityCheck:
    def __init__(self):
        # For local testing, use relative path to data directory
        self.forbidden_operations = ['rm', 'rmdir', 'delete']
        self.project_root = Path(__file__).parent.parent.parent
        self.allowed_paths = [
            self.project_root / "data",
            self.project_root
        ]

    def validate_operation(self, operation: str) -> bool:
        return not any(forbidden in operation.lower() 
                      for forbidden in self.forbidden_operations)

    def is_path_allowed(self, path: str) -> bool:
        try:
            path = Path(path).resolve()
            return any(
                str(path).startswith(str(allowed)) 
                for allowed in self.allowed_paths
            )
        except Exception:
            return False