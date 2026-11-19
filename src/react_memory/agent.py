from typing import Optional

from react_memory.block import MemoryFrame
from react_memory.context import AgentContext


class CustomAgentLoop:
    """Minimal agent loop that recompiles block-based memory on every step."""

    def __init__(
        self,
        memory_frame: MemoryFrame,
        ctx: Optional[AgentContext] = None,
    ) -> None:
        self.memory = memory_frame
        self.ctx = ctx if ctx is not None else AgentContext()

    def build_system_prompt(self) -> str:
        return self.memory.render(self.ctx) or ""

    def step(self, user_input: str) -> str:
        self.ctx.step += 1
        memory_snapshot = self.build_system_prompt()

        print(f"--- [Step {self.ctx.step}] Compiled Memory (input: {user_input!r}) ---")
        print(memory_snapshot)
        print("------------------------------------------")
        return memory_snapshot
