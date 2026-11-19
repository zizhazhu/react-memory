from dataclasses import dataclass, field
import os
from typing import Any


@dataclass
class AgentContext:
    """Shared mutable state consumed by memory blocks during rendering."""

    cwd: str = field(default_factory=os.getcwd)
    todos: list[dict[str, Any]] = field(default_factory=list)
    repo_files: list[str] = field(default_factory=list)
    step: int = 0
    extra: dict[str, Any] = field(default_factory=dict)
