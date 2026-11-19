import ast
import os

from react_memory.block import MemoryBlock
from react_memory.context import AgentContext


class RepoASTBlock(MemoryBlock):
    """Extracts top-level Python symbols (classes/functions) from tracked repo files."""

    tag = "repo_ast_outline"

    def should_render(self, ctx: AgentContext) -> bool:
        return len(ctx.repo_files) > 0

    def render_content(self, ctx: AgentContext) -> str:
        outlines: list[str] = []
        for filepath in ctx.repo_files:
            if not os.path.exists(filepath):
                continue
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read(), filename=filepath)
                symbols = [
                    f"  - {type(node).__name__}: {node.name}"
                    for node in ast.iter_child_nodes(tree)
                    if isinstance(
                        node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
                    )
                ]
                if symbols:
                    outlines.append(f"File: {filepath}\n" + "\n".join(symbols))
            except SyntaxError:
                outlines.append(f"File: {filepath} (SyntaxError)")
        return "\n\n".join(outlines)
