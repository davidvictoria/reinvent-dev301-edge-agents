# Strands Agents on the Edge 🏭

> **AWS re:Invent 2024 Session DEV301** | *AI agents at the edge: Build for offline, scale in cloud*

Build Generative AI agents that operate fully offline using the [Strands Agents SDK](https://github.com/strands-agents/sdk-python). Deploy lightweight local models with Ollama for remote manufacturing, field operations, and data sovereignty scenarios—then seamlessly scale to Claude on Amazon Bedrock when connectivity is available.

## What's Inside

### 📓 Jupyter Notebook (`strands_edge_demos.ipynb`)
Step-by-step demos covering core Strands SDK features:

| Demo | Feature | Description |
|------|---------|-------------|
| 1 | Tool Decorator | IoT device control with custom `@tool` functions |
| 2 | Structured Output | SCADA/MES data extraction with Pydantic models |
| 3 | Session Management | Persistent conversations for edge devices |
| 4 | MCP Integration | Local SQLite database for offline operation |

### 🏭 Edge Operator Agent (`e2e-demo/`)
Full-featured Streamlit application demonstrating a production-ready edge agent:

- **IoT Control**: Read sensors, control actuators via natural language
- **Document Search (RAG)**: Semantic search with ChromaDB + Ollama embeddings
- **Telemetry Database**: SQLite storage via MCP protocol
- **Model Switching**: Toggle local (Ollama) ↔ cloud (Bedrock) at runtime
- **Streaming Responses**: Real-time response streaming in the UI
- **Session Persistence**: Conversations survive restarts

```bash
cd e2e-demo && streamlit run streamlit_app.py
```

## Quick Start

### Prerequisites
- Python 3.10+
- [Ollama](https://ollama.ai) installed

### Setup

```bash
# 1. Install Ollama and pull models
ollama pull llama3.1
ollama pull nomic-embed-text
ollama serve

# 2. Install dependencies
pip install 'strands-agents[ollama]' strands-agents-tools pydantic mcp hypothesis chromadb streamlit
pip install uv  # Required for MCP SQLite server

# 3. Run the notebook demos
jupyter notebook strands_edge_demos.ipynb

# Or run the full Streamlit app
cd e2e-demo && pip install -e . && streamlit run streamlit_app.py
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Edge Operator Agent                       │
├─────────────────────────────────────────────────────────────┤
│  Streamlit UI (streaming responses)                         │
├─────────────────────────────────────────────────────────────┤
│  Strands Agent                                              │
│  ├── Model Router (Ollama ↔ Bedrock)                       │
│  ├── Session Manager (FileSessionManager)                   │
│  └── Tools:                                                 │
│      ├── IoT Tools (sensors, actuators)                    │
│      ├── Document Search (ChromaDB + embeddings)           │
│      ├── Database Tools (SQLite via MCP)                   │
│      └── SCADA Extraction (Pydantic structured output)     │
└─────────────────────────────────────────────────────────────┘
```

## Resources

- [Strands Agents SDK Documentation](https://strandsagents.com)
- [Ollama](https://ollama.ai)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io)
- [Amazon Bedrock](https://aws.amazon.com/bedrock/)

## Speakers

- Ana Cunha
- David Victoria

---

*Presented at AWS re:Invent 2024*
