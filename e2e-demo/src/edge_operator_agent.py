"""Edge Operator Agent - Main agent class integrating all capabilities.

Provides a unified conversational interface combining IoT device control,
structured data extraction, persistent sessions, and local database access.
"""

from typing import Optional, List, Any
import logging

from strands import Agent

from .config import EdgeAgentConfig
from .model_router import ModelRouter
from .session_manager import create_session_manager
from .tools.iot_tools import read_sensor, control_device, list_devices
from .tools.database_tools import DatabaseTools
from .tools.scada_extraction_tools import extract_scada_metrics

logger = logging.getLogger(__name__)

# System prompt for the Edge Operator Agent
SYSTEM_PROMPT = """You are an Edge Operator Agent, an AI assistant designed to help field operators 
manage industrial equipment and access information in manufacturing environments.

Your capabilities include:
1. **IoT Device Control**: Read sensor values and control actuators through natural language commands
   - Use read_sensor to get current readings from sensors
   - Use control_device to send commands to actuators
   - Use list_devices to see all available devices

2. **Structured Data Extraction**: Extract validated production metrics from SCADA reports
   - Use extract_scada_metrics to parse unstructured SCADA reports into structured data

3. **Local Database Operations**: Store and query device telemetry data
   - Use log_telemetry to record device readings
   - Use query_telemetry to retrieve historical data with filters
   - Use query_telemetry_aggregation for statistical analysis (AVG, MIN, MAX, COUNT)

When responding:
- Be concise and clear in your explanations
- Always confirm actions before executing device controls
- Provide relevant context about device readings
- Log important telemetry data for historical analysis
- Suggest next steps when appropriate

You operate locally on edge devices and can function fully offline using local models.
When cloud connectivity is available, you can switch to more powerful cloud models."""


class EdgeOperatorAgent:
    """Unified edge operator agent combining all capabilities.
    
    Integrates IoT device control, structured data extraction, session persistence,
    and local database access into a single conversational interface for field operators.
    
    Attributes:
        config: Configuration for the agent
        model_router: Routes inference to local or cloud models
        session_manager: Manages conversation persistence
        db_tools: Database tools for telemetry storage via MCP
        
    Requirements:
        - 3.1: Persist conversation state to local filesystem immediately
        - 3.2: Restore complete conversation history from local storage
        - 6.1: Initialize all tools and make them available
        - 6.2: Determine appropriate tools based on intent
    """
    
    def __init__(self, config: EdgeAgentConfig):
        """Initialize the EdgeOperatorAgent with all components.
        
        Args:
            config: Configuration containing session ID, storage paths,
                   and model configurations
        """
        self.config = config
        
        # Initialize model router for local/cloud switching
        self.model_router = ModelRouter(
            ollama_config=config.ollama_config,
            bedrock_config=config.bedrock_config
        )
        
        # Initialize session manager for conversation persistence
        # This creates the storage directory if it doesn't exist (Req 3.4)
        self.session_manager = create_session_manager(
            session_id=config.session_id,
            storage_dir=config.sessions_dir
        )
        
        # Initialize database tools for telemetry storage via MCP (Req 4.1, 4.2)
        self.db_tools = DatabaseTools(db_path=config.db_path)
        
        # Agent instance (created lazily)
        self._agent: Optional[Agent] = None
        
        # Track if we're using database tools context manager
        self._db_context_active = False
        
        logger.info(
            f"EdgeOperatorAgent initialized with session '{config.session_id}'"
        )
    
    def _get_tools(self) -> List[Any]:
        """Get the list of tools available to the agent.
        
        Combines all tool categories:
        - IoT tools: read_sensor, control_device, list_devices
        - SCADA extraction: extract_scada_metrics
        - Database tools: log_telemetry, query_telemetry, query_telemetry_aggregation
        
        Returns:
            List of tool functions for the agent to use
            
        Requirements:
            - 6.1: Initialize all tools and make them available
        """
        tools = [
            # IoT device control tools (Req 1.1, 1.2, 1.3)
            read_sensor,
            control_device,
            list_devices,
            # SCADA structured extraction tool (Req 2.1, 2.2)
            extract_scada_metrics,
        ]
        
        # Add database tools (Req 4.1, 4.2, 4.3, 4.4)
        tools.extend(self.db_tools.get_tools())
        
        return tools
    
    def _create_agent(self, agent_id: str = "default") -> Agent:
        """Create or recreate the agent with current model and session.
        
        Creates a new Agent instance with the current model from the
        model router, all available tools (IoT, database, SCADA extraction),
        and the session manager for conversation persistence.
        
        Args:
            agent_id: Unique identifier for the agent within the session
        
        Returns:
            Agent: Configured agent ready for use
            
        Requirements:
            - 3.1: Session manager persists state immediately
            - 3.2: Session manager restores history on agent creation
            - 6.1: All tools (IoT, database) initialized and available
            - 6.2: Agent determines appropriate tools based on intent
        """
        tools = self._get_tools()
        
        agent = Agent(
            model=self.model_router.get_model(),
            tools=tools,
            session_manager=self.session_manager,
            system_prompt=SYSTEM_PROMPT,
            agent_id=agent_id
        )
        
        logger.info(
            f"Agent created with {len(tools)} tools in "
            f"{self.model_router.mode} mode"
        )
        
        return agent
    
    @property
    def agent(self) -> Agent:
        """Get or create the agent instance.
        
        Lazily creates the agent on first access, ensuring all
        components are properly initialized.
        
        Returns:
            Agent: The active agent instance
        """
        if self._agent is None:
            self._agent = self._create_agent()
        return self._agent
    
    def set_model_mode(self, mode: str) -> tuple[bool, str]:
        """Switch between local and cloud model modes.
        
        When the mode changes successfully, updates the agent's model
        while preserving the session and all local capabilities
        (session persistence, database operations).
        
        Args:
            mode: Target mode ("local" or "cloud")
            
        Returns:
            Tuple of (success: bool, message: str) where:
            - success: True if mode was changed successfully, False otherwise
            - message: Description of the result or error
            
        Requirements:
            - 8.4: Apply change without requiring restart
            - 8.5: Display error and remain in local mode if cloud unavailable
            - 8.6: Preserve all local capabilities when in cloud mode
        """
        previous_mode = self.model_router.mode
        
        # Attempt to switch mode
        success = self.model_router.set_mode(mode)
        
        if success:
            # Update the existing agent's model instead of recreating
            # This preserves the session and avoids agent_id conflicts
            if self._agent is not None:
                self._agent.model = self.model_router.get_model()
            logger.info(f"Model mode changed from {previous_mode} to {mode}")
            return True, f"Successfully switched to {mode} mode"
        else:
            # Handle connectivity errors for cloud mode (Req 8.5)
            if mode == "cloud":
                error_msg = (
                    "Cannot switch to cloud mode: connectivity unavailable. "
                    "Remaining in local mode."
                )
            else:
                error_msg = f"Failed to switch to {mode} mode"
            
            logger.warning(error_msg)
            return False, error_msg
    
    def chat(self, message: str) -> str:
        """Process a user message and return the response.
        
        Sends the message to the agent, which determines the appropriate
        tools to invoke based on intent and orchestrates them to fulfill
        the request. The conversation is automatically persisted by the
        session manager after each interaction.
        
        The agent handles tool orchestration internally:
        - Analyzes the user's intent from the message
        - Selects appropriate tools (IoT, database, SCADA)
        - Executes tools in sequence when multiple are needed
        - Synthesizes tool outputs into a coherent response
        
        Args:
            message: The user's input message
            
        Returns:
            The agent's response as a string, synthesizing tool outputs
            into a coherent natural language response
            
        Requirements:
            - 3.1: Conversation persisted immediately after processing
            - 6.2: Agent determines appropriate tools based on intent
            - 6.3: Agent orchestrates multiple tools in sequence when needed
            - 6.4: Coherent natural language response synthesizing tool outputs
            - 6.5: Handle errors gracefully and inform the operator
        """
        try:
            response = self.agent(message)
            return str(response)
        except Exception as e:
            # Handle errors gracefully (Req 6.5)
            logger.error(f"Error processing message: {e}")
            return f"I encountered an error processing your request: {str(e)}"
    
    async def stream_chat(self, message: str):
        """Process a user message and stream the response.
        
        Async generator that yields text chunks as they are generated
        by the agent. Enables real-time streaming display in UIs.
        
        Args:
            message: The user's input message
            
        Yields:
            Text chunks as they are generated
            
        Requirements:
            - 6.4: Provide coherent natural language response display
            - 6.5: Handle errors gracefully and inform the operator
        """
        try:
            async for event in self.agent.stream_async(message):
                # TextStreamEvent stores text in 'data' key
                if isinstance(event, dict) and 'data' in event:
                    text = event.get('data')
                    if isinstance(text, str) and text:
                        yield text
        except Exception as e:
            logger.error(f"Error streaming message: {e}")
            yield f"I encountered an error processing your request: {str(e)}"
    
    @property
    def current_mode(self) -> str:
        """Get the current model mode.
        
        Returns:
            The current mode ("local" or "cloud")
        """
        return self.model_router.mode
    
    def __enter__(self):
        """Enter the context manager, starting the MCP client for database tools."""
        self.db_tools.__enter__()
        self._db_context_active = True
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context manager, stopping the MCP client."""
        self._db_context_active = False
        return self.db_tools.__exit__(exc_type, exc_val, exc_tb)
