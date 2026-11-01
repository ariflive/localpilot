import os
import tempfile
from pathlib import Path
from app.services.workspace_guard import workspace_guard


def test_normal_permitted_access():
    with tempfile.TemporaryDirectory(dir=os.getcwd()) as tmpdir:
        test_file = os.path.join(tmpdir, "test.txt")
        Path(test_file).write_text("hello")
        safe, result = workspace_guard.is_path_safe(test_file)
        assert safe is True


def test_parent_directory_traversal():
    safe, result = workspace_guard.is_path_safe("../../../etc/passwd")
    assert safe is False


def test_absolute_path_outside_workspace():
    safe, result = workspace_guard.is_path_safe("C:/Windows/System32/cmd.exe")
    assert safe is False


def test_sensitive_file_env():
    safe, result = workspace_guard.is_path_safe(".env")
    assert safe is False


def test_sensitive_file_db():
    safe, result = workspace_guard.is_path_safe("localpilot.db")
    assert safe is False


def test_invalid_path():
    safe, result = workspace_guard.is_path_safe("")
    assert safe is False or isinstance(result, str)
