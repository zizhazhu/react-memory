from react_memory.block import MemoryBlock
from react_memory.context import AgentContext


class CwdBlock(MemoryBlock):
    """Displays the current working directory."""

    tag = "environment_cwd"

    def render_content(self, ctx: AgentContext) -> str:
        return f"Current Working Directory: {ctx.cwd}"
