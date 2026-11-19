from react_memory.block import MemoryBlock
from react_memory.context import AgentContext


class TodoBlock(MemoryBlock):
    """Displays the current task checklist when non-empty."""

    tag = "current_todos"

    def should_render(self, ctx: AgentContext) -> bool:
        return len(ctx.todos) > 0

    def render_content(self, ctx: AgentContext) -> str:
        lines: list[str] = []
        for i, item in enumerate(ctx.todos, 1):
            status = "[x]" if item.get("done") else "[ ]"
            lines.append(f"{i}. {status} {item['task']}")
        return "\n".join(lines)
