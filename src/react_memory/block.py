from abc import ABC, abstractmethod
from typing import Optional

from react_memory.context import AgentContext


class MemoryBlock(ABC):
    """Base class for a composable, reactive memory block."""

    tag: str = "block"

    def should_render(self, ctx: AgentContext) -> bool:
        """Return False to omit this block from the compiled memory."""
        return True

    @abstractmethod
    def render_content(self, ctx: AgentContext) -> str:
        """Produce the inner body of this block for the current context."""

    def render(self, ctx: AgentContext) -> Optional[str]:
        """Render the block wrapped in its XML-like tag, or None if omitted/empty."""
        if not self.should_render(ctx):
            return None
        content = self.render_content(ctx).strip()
        if not content:
            return None
        return f"<{self.tag}>\n{content}\n</{self.tag}>"


class MemoryFrame(MemoryBlock):
    """Composite memory block that groups and renders child blocks."""

    def __init__(
        self,
        tag: str = "agent_memory",
        children: Optional[list[MemoryBlock]] = None,
    ) -> None:
        self.tag = tag
        self.children: list[MemoryBlock] = list(children) if children else []

    def add(self, block: MemoryBlock) -> "MemoryFrame":
        self.children.append(block)
        return self

    def render_content(self, ctx: AgentContext) -> str:
        rendered_parts: list[str] = []
        for child in self.children:
            part = child.render(ctx)
            if part:
                rendered_parts.append(part)
        return "\n\n".join(rendered_parts)
