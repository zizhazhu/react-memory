from pathlib import Path

from react_memory import (
    CustomAgentLoop,
    CwdBlock,
    MemoryFrame,
    RepoASTBlock,
    TodoBlock,
)


def main() -> None:
    memory_layout = MemoryFrame(
        tag="memory_system",
        children=[
            MemoryFrame(
                tag="workspace_state",
                children=[
                    CwdBlock(),
                    RepoASTBlock(),
                ],
            ),
            TodoBlock(),
        ],
    )

    agent = CustomAgentLoop(memory_frame=memory_layout)
    agent.ctx.todos = [
        {"task": "Implement dsh agent loop plugin interface", "done": True},
        {"task": "Integrate incremental AST update mechanism", "done": False},
    ]

    block_file = Path(__file__).resolve().parent.parent / "src" / "react_memory" / "blocks" / "todo.py"
    agent.ctx.repo_files = [str(block_file)]

    # Step 1: initial compiled memory
    agent.step("Check the implementation of TodoBlock")

    # External state changes -> mutate context in place instead of appending dialogue
    agent.ctx.todos[1]["done"] = True
    agent.ctx.todos.append({"task": "Add reactive diffing", "done": False})

    # Step 2: memory blocks re-render with updated state in place
    agent.step("Continue with next task")


if __name__ == "__main__":
    main()
