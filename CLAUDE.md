# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

A 6-week AI Agentic Engineering course by Ed Donner. Each week covers a different agent framework via Jupyter notebooks (`N_labN.ipynb`) and standalone Python examples. Community contributions live in subdirectories alongside the course material.

## Environment Setup

- **Python**: 3.12 (pinned in `.python-version`)
- **Package manager**: `uv` — dependencies declared in `pyproject.toml`, locked in `requirements.txt`
- **Virtual environment**: `.venv/` at repo root

Activate the venv:
```bash
source .venv/bin/activate
```

Install/sync dependencies:
```bash
uv sync
```

## Running Code

Most course material runs interactively in Jupyter:
```bash
jupyter notebook
```

Standalone Python files (Gradio apps, MCP servers, agents) run directly:
```bash
python 1_foundations/app.py
python 6_mcp/traders.py
```

### Week 3 (CrewAI) — special setup required

```bash
# Install CrewAI as a uv global tool (run once)
uv tool install crewai==0.130.0 --python 3.12

# Run a CrewAI project
cd 3_crew/debate
crewai run
```

### Environment variables

API keys go in a `.env` file at the repo root. Common keys:
- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `GOOGLE_API_KEY` / `GEMINI_API_KEY` (Gemini users need both keys for CrewAI week)

Validate the environment:
```bash
python setup/diagnostics.py
```

## Module Architecture

| Week | Directory | Framework | Key files |
|------|-----------|-----------|-----------|
| 1 | `1_foundations/` | Raw OpenAI + function calling | `app.py` (Gradio chatbot) |
| 2 | `2_openai/` | OpenAI Agents SDK | Lab notebooks, deep-research project |
| 3 | `3_crew/` | CrewAI | `debate/`, `coder/`, `stock_picker/`, `engineering_team/`, `financial_researcher/` |
| 4 | `4_langgraph/` | LangGraph | `sidekick.py` (worker/evaluator loop), `sidekick_tools.py` (Playwright) |
| 5 | `5_autogen/` | AutoGen | `agent.py`, `creator.py`, `world.py` |
| 6 | `6_mcp/` | MCP + OpenAI Agents SDK | `traders.py`, `app.py` (Gradio dashboard), `accounts_server.py`, `market_server.py` |

### Architectural progression

- **Week 1**: Manual JSON tool schemas → function dispatch
- **Week 2**: OpenAI Agents SDK handles tool binding and execution loops
- **Week 3**: CrewAI YAML configs declare agents, tasks, and crews declaratively
- **Week 4**: LangGraph `StateGraph` with `TypedDict` state, conditional edges, SQLite checkpoint memory
- **Week 5**: AutoGen `RoutedAgent` / `AssistantAgent` with message-passing between agents
- **Week 6**: MCP servers (stdio transport) expose tools/resources; agents connect via `MCPServerStdio`

### CrewAI project structure

Each project under `3_crew/` follows the standard CrewAI layout:
```
<project>/
  src/<project>/
    config/agents.yaml   # agent definitions
    config/tasks.yaml    # task definitions
    crew.py              # @CrewBase class wiring agents + tasks
    main.py              # entrypoint
```

### LangGraph pattern (Week 4)

`sidekick.py` implements a **worker → tool node → evaluator** loop:
- State is a `TypedDict` with accumulated messages
- `MemorySaver` (SQLite) provides persistent, resumable checkpoints
- Playwright tools in `sidekick_tools.py` for web automation

### MCP pattern (Week 6)

`traders.py` spawns MCP servers as subprocesses and connects agents via `MCPServerStdio`. Multiple LLM providers (OpenAI, Anthropic) can be mixed. `app.py` provides a Gradio dashboard for real-time monitoring.

## No Formal Test Suite

Labs are designed for interactive, manual execution. There is no pytest configuration at the repo root.
