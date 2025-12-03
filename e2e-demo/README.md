# Edge Operator Agent 🏭

An AI-powered assistant for industrial equipment management built with the [Strands Agents SDK](https://github.com/strands-agents/strands-agents). The agent operates fully offline on edge devices, combining IoT device control, structured data extraction, persistent sessions, local database access, and local document search capabilities.

> **Demo project** showcasing Strands Agents SDK capabilities for edge/industrial scenarios with real-time streaming responses.

## Features

- **IoT Device Control**: Read sensors and control actuators via natural language
- **Structured Data Extraction**: Extract validated SCADA/MES data with Pydantic schemas
- **Session Persistence**: Conversations persist across restarts using FileSessionManager
- **Local Database**: Store and query telemetry data in SQLite via MCP
- **Document Search (RAG)**: Semantic search of technical documentation using ChromaDB
- **Dynamic Model Switching**: Toggle between local (Ollama) and cloud (Claude on Bedrock) models
- **Real-time Streaming**: Responses stream in real-time for better UX

## Prerequisites

### Required Software

1. **Python 3.10+**
   ```bash
   python --version  # Should be 3.10 or higher
   ```

2. **Ollama** (for local inference)
   ```bash
   # macOS
   brew install ollama
   
   # Linux
   curl -fsSL https://ollama.com/install.sh | sh
   ```

3. **Required Ollama Models**
   ```bash
   # Pull the LLM model (lightweight, optimized for edge)
   ollama pull hoangquan456/qwen3-nothink:4b
   
   # Pull the embedding model
   ollama pull nomic-embed-text
   ```

4. **UV Package Manager** (for MCP SQLite server)
   ```bash
   # macOS
   brew install uv
   
   # Or via pip
   pip install uv
   ```

### Optional (for Cloud Mode)

- AWS credentials configured for Amazon Bedrock access
- Access to Claude models in your AWS region

## Installation

1. **Clone the repository and navigate to the demo directory:**
   ```bash
   cd e2e-demo
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -e .
   ```

4. **Start Ollama server:**
   ```bash
   ollama serve
   ```

## Running the Application

### Streamlit Web Interface (Recommended)

```bash
cd e2e-demo
streamlit run streamlit_app.py
```

The web interface will open at `http://localhost:8501` with:
- Chat interface for interacting with the agent
- Model mode toggle (Local/Cloud) in the sidebar
- Document upload for indexing technical manuals

### Command Line Interface

```bash
cd e2e-demo
python -m src.edge_operator_agent
```

## Project Structure

```
e2e-demo/
├── src/
│   ├── __init__.py
│   ├── app.py                    # Streamlit app module
│   ├── config.py                 # Configuration dataclass
│   ├── edge_operator_agent.py    # Main agent class
│   ├── model_router.py           # Local/Cloud model switching
│   ├── session_manager.py        # Session persistence
│   ├── models/
│   │   ├── device_registry.py    # IoT device definitions
│   │   ├── document_chunk.py     # Document chunk model
│   │   ├── iot_devices.py        # IoT device dataclasses
│   │   └── scada_models.py       # SCADA/MES Pydantic models
│   ├── storage/
│   │   └── __init__.py
│   └── tools/
│       ├── database_tools.py     # MCP SQLite tools
│       ├── document_search_tools.py  # ChromaDB RAG tools
│       ├── iot_tools.py          # Sensor/actuator tools
│       └── scada_extraction_tools.py # Structured extraction
├── documents/                    # Sample technical documents
│   ├── conveyor_belt_manual.md
│   ├── packaging_unit_manual.md
│   ├── safety_procedures.md
│   └── troubleshooting_guide.md
├── tests/
│   └── test_session_manager.py
├── pyproject.toml
├── streamlit_app.py              # Entry point for Streamlit
└── README.md
```

## Configuration

The agent is configured via `EdgeAgentConfig` in `src/config.py`:

```python
@dataclass
class EdgeAgentConfig:
    session_id: str                           # Unique session identifier
    sessions_dir: str = "./sessions"          # Session storage path
    db_path: str = "./telemetry.db"          # SQLite database path
    vector_store_path: str = "./vector_store" # ChromaDB storage path
    documents_dir: str = "./documents"        # Source documents path
    embedding_model: str = "nomic-embed-text" # Ollama embedding model
    ollama_config: dict = ...                 # Ollama model settings
    bedrock_config: dict = ...                # AWS Bedrock settings
```

## Demo Interactions

See [DEMO_SCRIPT.md](./DEMO_SCRIPT.md) for detailed example interactions demonstrating each capability.

### Quick Examples

**1. List Available Devices**
```
User: What devices are available?
Agent: Here are the available IoT devices:
- temp-sensor-001 (sensor) - Location: Production Line A
- humidity-sensor-001 (sensor) - Location: Warehouse B
- valve-actuator-001 (actuator) - Location: Cooling System
```

**2. Read Sensor Values**
```
User: What's the current temperature on Production Line A?
Agent: Reading from temp-sensor-001...
Temperature: 23.5°C at Production Line A
```

**3. Control Actuators**
```
User: Open the cooling valve
Agent: Sending command to valve-actuator-001...
Valve actuator set to OPEN state. Previous state was CLOSED.
```

**4. Search Documentation**
```
User: How do I troubleshoot a belt tracking issue?
Agent: Based on the equipment documentation:
[Returns relevant sections from conveyor_belt_manual.md]
```

**5. Query Telemetry Data**
```
User: Show me the average temperature readings from today
Agent: Querying telemetry database...
Average temperature: 24.2°C (from 48 readings)
```

## Troubleshooting

### Ollama Connection Issues

```
Error: Could not connect to Ollama
```
**Solution**: Ensure Ollama is running:
```bash
ollama serve
```

### Model Not Found

```
Error: Model not found
```
**Solution**: Pull the required model:
```bash
ollama pull hoangquan456/qwen3-nothink:4b
```

### MCP SQLite Server Issues

```
Error: MCP server failed to start
```
**Solution**: Ensure `uvx` is installed and working:
```bash
uvx --version
uvx mcp-server-sqlite --help
```

### Cloud Mode Unavailable

```
Error: Cloud connectivity unavailable
```
**Solution**: 
1. Check AWS credentials are configured
2. Verify Bedrock access in your region
3. The agent will remain in Local mode if cloud is unavailable

## Development

### Running Tests

```bash
cd e2e-demo
pytest tests/ -v
```

### Property-Based Tests

The project uses Hypothesis for property-based testing:
```bash
pytest tests/ -v -k "property"
```

## License

MIT License - See LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request
