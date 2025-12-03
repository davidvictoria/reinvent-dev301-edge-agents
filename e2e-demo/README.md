# Edge Operator Agent 🏭

An AI-powered assistant for industrial equipment management built with the [Strands Agents SDK](https://github.com/strands-agents/strands-agents). The agent operates fully offline on edge devices, combining IoT device control, structured data extraction, persistent sessions, and local database access.

> **Demo project** showcasing Strands Agents SDK capabilities for edge/industrial scenarios with real-time streaming responses.

## Features

- **IoT Device Control**: Read sensors and control actuators via natural language
- **Structured Data Extraction**: Extract validated SCADA/MES data with Pydantic schemas
- **Session Persistence**: Conversations persist across restarts using FileSessionManager
- **Local Database**: Store and query telemetry data in SQLite via MCP
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

3. **Required Ollama Model**
   ```bash
   # Pull the LLM model (lightweight, optimized for edge)
   ollama pull hoangquan456/qwen3-nothink:4b
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
│   ├── config.py                 # Configuration dataclass
│   ├── edge_operator_agent.py    # Main agent class
│   ├── model_router.py           # Local/Cloud model switching
│   ├── session_manager.py        # Session persistence
│   ├── models/
│   │   ├── device_registry.py    # IoT device definitions
│   │   ├── iot_devices.py        # IoT device dataclasses
│   │   └── scada_models.py       # SCADA/MES Pydantic models
│   └── tools/
│       ├── database_tools.py     # MCP SQLite tools
│       ├── iot_tools.py          # Sensor/actuator tools
│       └── scada_extraction_tools.py # Structured extraction
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
    ollama_config: dict = ...                 # Ollama model settings
    bedrock_config: dict = ...                # AWS Bedrock settings
```

## Demo Interactions

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

**4. Query Telemetry Data**
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

## License

MIT License - See LICENSE file for details.
