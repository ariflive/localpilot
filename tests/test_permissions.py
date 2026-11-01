from app.services.permission_manager import permission_manager


def test_permission_denies_unregistered_tool():
    allowed, msg = permission_manager.validate_tool_call("rm_rf_everything", {})
    assert allowed is False
    assert "not in allowlist" in msg.lower() or "not allowed" in msg.lower()


def test_permission_denies_shell_if_attempted():
    allowed, msg = permission_manager.validate_tool_call("shell", {"cmd": "ls"})
    assert allowed is False
