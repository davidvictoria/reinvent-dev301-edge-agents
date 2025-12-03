"""Configuration module for Edge Operator Agent.

Provides the EdgeAgentConfig dataclass for configuring all agent components
including model providers and storage paths.
"""

from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class EdgeAgentConfig:
    """Configuration for the Edge Operator Agent.
    
    Attributes:
        session_id: Unique identifier for the conversation session
        sessions_dir: Directory path for storing session data
        db_path: Path to the SQLite telemetry database
        ollama_config: Configuration dict for local Ollama model
        bedrock_config: Configuration dict for AWS Bedrock model
    """
    session_id: str
    sessions_dir: str = "./sessions"
    db_path: str = "./telemetry.db"
    ollama_config: Dict[str, Any] = field(default_factory=lambda: {
        "host": "http://localhost:11434",
        "model_id": "hoangquan456/qwen3-nothink:4b",
        "temperature": 0.7,
        "keep_alive": "10m"
    })
    bedrock_config: Dict[str, Any] = field(default_factory=lambda: {
        "model_id": "anthropic.claude-3-sonnet-20240229-v1:0",
        "region_name": "us-east-1"
    })
