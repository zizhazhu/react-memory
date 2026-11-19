# react-memory

A block-based, reactive memory model for LLM context management.

## Concept

Traditional LLM systems rely on an **append-only context**: every new event, state change, or interaction is stacked onto the end of a linear conversation history. Over time, this leads to context bloat, redundant or conflicting information, and degraded reasoning.

**react-memory** takes a different approach:

- **Block-Based Memory**: Instead of a monolithic, ever-growing message log, memory is composed of discrete, modular blocks—assembled piece by piece like building blocks.
- **Reactive In-Place Updates**: When external state changes, you directly update the content of the corresponding memory block rather than appending new dialogue turns to patch over old state.

### Append-Only vs. Block-Based

| | Append-Only Context | react-memory |
| :--- | :--- | :--- |
| **Structure** | Linear, stacked message history | Composable, modular memory blocks |
| **State Changes** | Append new messages to the end | Update the relevant block directly in place |
| **Context State** | Accumulates stale/conflicting info | Stays concise, consistent, and up to date |
