"""Model Router for Edge Operator Agent.

Provides dynamic switching between local (Ollama) and cloud (Bedrock) model providers.
Supports lazy-loading of cloud models and connectivity checking.
"""

from typing import Literal, Dict, Any, Union
import socket
import logging

from strands.models.ollama import OllamaModel

logger = logging.getLogger(__name__)

# Type alias for model mode
ModelMode = Literal["local", "cloud"]


class ModelRouter:
    """Routes inference requests to the appropriate model provider.
    
    Supports dynamic switching between local Ollama models and cloud-based
    Amazon Bedrock models. The Bedrock model is lazy-loaded only when cloud
    mode is first selected.
    
    Attributes:
        ollama_model: The local Ollama model instance
        bedrock_model: The cloud Bedrock model instance (lazy-loaded)
        current_mode: Current routing mode ("local" or "cloud")
        bedrock_config: Configuration dict for Bedrock model initialization
    """
    
    def __init__(
        self,
        ollama_config: Dict[str, Any],
        bedrock_config: Dict[str, Any]
    ):
        """Initialize the ModelRouter with model configurations.
        
        Args:
            ollama_config: Configuration dict for OllamaModel.
                Expected keys: host, model_id, temperature, keep_alive
            bedrock_config: Configuration dict for BedrockModel.
                Expected keys: model_id, region_name
        """
        # Initialize local Ollama model immediately
        self.ollama_model = OllamaModel(
            host=ollama_config.get("host", "http://localhost:11434"),
            model_id=ollama_config.get("model_id", "llama3.1"),
            temperature=ollama_config.get("temperature"),
            keep_alive=ollama_config.get("keep_alive", "10m")
        )
        
        # Store Bedrock config for lazy initialization
        self.bedrock_config = bedrock_config
        self.bedrock_model = None  # Lazy-loaded when cloud mode selected
        
        # Default to local mode for offline-first operation (Requirement 8.7)
        self.current_mode: ModelMode = "local"

    def get_model(self) -> Union[OllamaModel, Any]:
        """Returns the currently active model based on the current mode.
        
        Returns:
            The active model instance (OllamaModel for local, BedrockModel for cloud)
        
        Note:
            When in cloud mode, this will lazy-load the BedrockModel if not
            already initialized.
        """
        if self.current_mode == "local":
            return self.ollama_model
        return self._get_bedrock_model()
    
    def _get_bedrock_model(self) -> Any:
        """Lazy-load and return the Bedrock model.
        
        The BedrockModel is only imported and instantiated when first needed,
        reducing startup time and avoiding unnecessary AWS SDK initialization
        when running in local-only mode.
        
        Returns:
            The BedrockModel instance
        """
        if self.bedrock_model is None:
            from strands.models.bedrock import BedrockModel
            
            self.bedrock_model = BedrockModel(
                model_id=self.bedrock_config.get(
                    "model_id", 
                    "anthropic.claude-3-sonnet-20240229-v1:0"
                ),
                region_name=self.bedrock_config.get("region_name", "us-east-1")
            )
            logger.info("BedrockModel initialized for cloud inference")
        
        return self.bedrock_model
    
    def set_mode(self, mode: ModelMode) -> bool:
        """Switch between local and cloud model modes.
        
        When switching to cloud mode, performs a connectivity check first.
        If connectivity is unavailable, the mode remains unchanged.
        
        Args:
            mode: The target mode ("local" or "cloud")
            
        Returns:
            True if the mode was successfully changed, False otherwise
            
        Note:
            Switching to local mode always succeeds.
            Switching to cloud mode requires network connectivity.
        """
        if mode == "local":
            self.current_mode = "local"
            logger.info("Switched to local mode (Ollama)")
            return True
        
        if mode == "cloud":
            if not self._check_connectivity():
                logger.warning(
                    "Cannot switch to cloud mode: connectivity unavailable"
                )
                return False
            
            # Ensure Bedrock model is initialized
            self._get_bedrock_model()
            self.current_mode = "cloud"
            logger.info("Switched to cloud mode (Bedrock)")
            return True
        
        logger.error(f"Invalid mode: {mode}")
        return False
    
    def _check_connectivity(self) -> bool:
        """Check if cloud connectivity is available.
        
        Performs a simple socket connection test to verify network access
        to AWS services.
        
        Returns:
            True if connectivity is available, False otherwise
        """
        try:
            # Try to connect to AWS Bedrock endpoint
            # Using bedrock.us-east-1.amazonaws.com as a test endpoint
            region = self.bedrock_config.get("region_name", "us-east-1")
            host = f"bedrock-runtime.{region}.amazonaws.com"
            
            socket.create_connection((host, 443), timeout=5)
            return True
        except (socket.timeout, socket.error, OSError) as e:
            logger.debug(f"Connectivity check failed: {e}")
            return False
    
    @property
    def mode(self) -> ModelMode:
        """Get the current model mode.
        
        Returns:
            The current mode ("local" or "cloud")
        """
        return self.current_mode
