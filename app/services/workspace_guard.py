import os
from pathlib import Path
from typing import Tuple


class WorkspaceGuard:
    def __init__(self, workspace_root: str = None):
        if workspace_root is None:
            # Default to project root
            self.workspace_root = Path(os.path.abspath(os.getcwd()))
        else:
            self.workspace_root = Path(os.path.abspath(workspace_root))
        self.workspace_root = self.workspace_root.resolve()
        # Sensitive patterns to block
        self.sensitive_patterns = [
            ".env", ".env.local", ".env.production",
            "id_rsa", "id_dsa", "private_key", ".pem", ".key",
            "credentials", "secrets",
        ]
        self.sensitive_extensions = [".db", ".sqlite", ".sqlite3", ".log"]
        self.sensitive_dirs = ["logs", ".venv", "venv", "__pycache__"]

    def is_path_safe(self, path: str) -> Tuple[bool, str]:
        try:
            # Reject if contains traversal patterns
            if ".." in path:
                return False, "Path traversal not allowed"
            # Resolve the path
            requested = Path(path)
            if requested.is_absolute():
                # Check if it's within workspace
                try:
                    resolved = requested.resolve(strict=False)
                except Exception:
                    return False, "Invalid path"
                if not self._is_under_workspace(resolved):
                    return False, "Access outside workspace not allowed"
            else:
                # Relative path - resolve relative to workspace
                resolved = (self.workspace_root / requested).resolve(strict=False)
            # Check if under workspace
            if not self._is_under_workspace(resolved):
                return False, "Access outside workspace not allowed"
            # Check for symlink escapes
            try:
                if resolved.is_symlink():
                    real_path = resolved.resolve(strict=False)
                    if not self._is_under_workspace(real_path):
                        return False, "Symlink escape not allowed"
            except Exception:
                pass
            # Check sensitive files
            name = resolved.name.lower()
            str_path = str(resolved).lower()
            for pattern in self.sensitive_patterns:
                if pattern in name or pattern in str_path:
                    return False, "Access to sensitive file not allowed"
            for ext in self.sensitive_extensions:
                if str_path.endswith(ext):
                    # Allow if it's in test/temp and explicitly needed, but block by default
                    if "test" not in str_path and "tmp" not in str_path:
                        return False, "Access to sensitive file not allowed"
            for sdir in self.sensitive_dirs:
                if sdir in str_path and "test" not in str_path:
                    return False, "Access to restricted directory not allowed"
            return True, str(resolved)
        except Exception:
            return False, "Invalid path"

    def _is_under_workspace(self, path: Path) -> bool:
        try:
            path_str = str(path.resolve())
            workspace_str = str(self.workspace_root.resolve())
            return path_str.startswith(workspace_str + os.sep) or path_str == workspace_str
        except Exception:
            return False


workspace_guard = WorkspaceGuard()
