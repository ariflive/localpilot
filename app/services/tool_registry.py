from typing import Dict, Any, List, Optional


class Tool:
    def __init__(self, name: str, description: str, requires_approval: bool = False, allowed: bool = True):
        self.name = name
        self.description = description
        self.requires_approval = requires_approval
        self.allowed = allowed


class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Tool] = {}
        self._register_defaults()

    def _register_defaults(self):
        # Explicit allowlist - NO shell, NO python exec
        self.register_tool("read_file", "Read a file from workspace", requires_approval=False)
        self.register_tool("list_files", "List files in directory", requires_approval=False)
        self.register_tool("search_files", "Search for files by pattern", requires_approval=False)
        self.register_tool("search_content", "Search content in files", requires_approval=False)
        self.register_tool("web_search", "Search web (if needed)", requires_approval=True)
        self.register_tool("create_note", "Create a note", requires_approval=False)

    def register_tool(self, name: str, description: str, requires_approval: bool = False):
        self._tools[name] = Tool(name, description, requires_approval)

    def get_tool(self, name: str) -> Optional[Tool]:
        return self._tools.get(name)

    def list_tools(self) -> List[Dict[str, Any]]:
        return [
            {"name": t.name, "description": t.description, "requires_approval": t.requires_approval}
            for t in self._tools.values()
        ]

    def is_allowed(self, name: str) -> bool:
        return name in self._tools


tool_registry = ToolRegistry()
