from pathlib import Path

from react_memory import (
    AgentContext,
    CustomAgentLoop,
    CwdBlock,
    MemoryFrame,
    RepoASTBlock,
    TodoBlock,
)


def test_cwd_block_renders_current_directory() -> None:
    ctx = AgentContext(cwd="/tmp/workspace")
    rendered = CwdBlock().render(ctx)
    assert rendered == (
        "<environment_cwd>\n"
        "Current Working Directory: /tmp/workspace\n"
        "</environment_cwd>"
    )


def test_todo_block_omitted_when_empty_and_updates_in_place() -> None:
    ctx = AgentContext()
    block = TodoBlock()
    assert block.render(ctx) is None

    ctx.todos = [
        {"task": "Task A", "done": False},
        {"task": "Task B", "done": True},
    ]
    assert block.render(ctx) == (
        "<current_todos>\n"
        "1. [ ] Task A\n"
        "2. [x] Task B\n"
        "</current_todos>"
    )

    # In-place mutation updates the block directly
    ctx.todos[0]["done"] = True
    assert block.render(ctx) == (
        "<current_todos>\n"
        "1. [x] Task A\n"
        "2. [x] Task B\n"
        "</current_todos>"
    )


def test_repo_ast_block_parses_symbols_and_handles_syntax_errors(tmp_path: Path) -> None:
    valid_file = tmp_path / "sample.py"
    valid_file.write_text(
        "class Foo:\n"
        "    pass\n\n"
        "def bar():\n"
        "    return 1\n\n"
        "async def baz():\n"
        "    return 2\n",
        encoding="utf-8",
    )
    broken_file = tmp_path / "broken.py"
    broken_file.write_text("def broken(:\n", encoding="utf-8")
    missing_file = tmp_path / "missing.py"

    ctx = AgentContext(
        repo_files=[str(valid_file), str(broken_file), str(missing_file)]
    )
    rendered = RepoASTBlock().render(ctx)
    assert rendered is not None
    assert f"File: {valid_file}" in rendered
    assert "  - ClassDef: Foo" in rendered
    assert "  - FunctionDef: bar" in rendered
    assert "  - AsyncFunctionDef: baz" in rendered
    assert f"File: {broken_file} (SyntaxError)" in rendered
    assert str(missing_file) not in rendered


def test_memory_frame_composition_and_agent_loop(tmp_path: Path) -> None:
    sample_file = tmp_path / "mod.py"
    sample_file.write_text("def hello():\n    pass\n", encoding="utf-8")

    layout = MemoryFrame(
        tag="memory_system",
        children=[
            MemoryFrame(
                tag="workspace_state",
                children=[CwdBlock(), RepoASTBlock()],
            ),
            TodoBlock(),
        ],
    )
    agent = CustomAgentLoop(memory_frame=layout)
    agent.ctx.cwd = str(tmp_path)
    agent.ctx.repo_files = [str(sample_file)]

    snap1 = agent.step("First step")
    assert agent.ctx.step == 1
    assert "<memory_system>" in snap1
    assert "<workspace_state>" in snap1
    assert "<environment_cwd>" in snap1
    assert "<repo_ast_outline>" in snap1
    assert "<current_todos>" not in snap1

    agent.ctx.todos.append({"task": "Write tests", "done": False})
    snap2 = agent.step("Second step")
    assert agent.ctx.step == 2
    assert "<current_todos>\n1. [ ] Write tests\n</current_todos>" in snap2
