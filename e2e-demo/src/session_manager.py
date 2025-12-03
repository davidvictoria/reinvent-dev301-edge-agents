"""Session management module for Edge Operator Agent.

Provides session persistence functionality using Strands FileSessionManager
with configurable storage directory and automatic directory creation.
"""

import os
from pathlib import Path
from typing import Optional

from strands.session.file_session_manager import FileSessionManager


def create_session_manager(
    session_id: str,
    storage_dir: str = "./edge_sessions"
) -> FileSessionManager:
    """Create a FileSessionManager with automatic directory creation.
    
    Creates the storage directory if it doesn't exist, then initializes
    a FileSessionManager for persisting conversation state.
    
    Args:
        session_id: Unique identifier for the conversation session
        storage_dir: Directory path for storing session data.
                    Defaults to "./edge_sessions"
    
    Returns:
        FileSessionManager: Configured session manager ready for use with an Agent
    
    Requirements:
        - 3.1: Persist conversation state to local filesystem immediately
        - 3.4: Create directory structure automatically if it doesn't exist
    
    Example:
        >>> session_manager = create_session_manager(
        ...     session_id="operator-001",
        ...     storage_dir="./sessions"
        ... )
        >>> agent = Agent(session_manager=session_manager)
    """
    # Ensure storage directory exists (Requirement 3.4)
    storage_path = Path(storage_dir)
    storage_path.mkdir(parents=True, exist_ok=True)
    
    # Create and return the FileSessionManager (Requirement 3.1)
    return FileSessionManager(
        session_id=session_id,
        storage_dir=str(storage_path)
    )


class EdgeSessionManager:
    """Wrapper class for managing Edge Operator Agent sessions.
    
    Provides a higher-level interface for session management with
    automatic directory creation and session lifecycle management.
    
    Attributes:
        session_id: Unique identifier for the session
        storage_dir: Directory path where sessions are stored
        session_manager: The underlying FileSessionManager instance
    
    Requirements:
        - 3.1: Persist conversation state to local filesystem
        - 3.4: Create directory structure automatically
        - 3.5: Isolate each session's data by session ID
    """
    
    def __init__(
        self,
        session_id: str,
        storage_dir: str = "./edge_sessions"
    ):
        """Initialize the EdgeSessionManager.
        
        Args:
            session_id: Unique identifier for the conversation session
            storage_dir: Directory path for storing session data
        """
        self.session_id = session_id
        self.storage_dir = storage_dir
        self._session_manager: Optional[FileSessionManager] = None
    
    @property
    def session_manager(self) -> FileSessionManager:
        """Get or create the FileSessionManager instance.
        
        Lazily initializes the session manager on first access,
        ensuring the storage directory exists.
        
        Returns:
            FileSessionManager: The configured session manager
        """
        if self._session_manager is None:
            self._session_manager = create_session_manager(
                session_id=self.session_id,
                storage_dir=self.storage_dir
            )
        return self._session_manager
    
    def get_session_path(self) -> Path:
        """Get the path to this session's storage directory.
        
        Returns:
            Path: The directory path where this session's data is stored
        """
        return Path(self.storage_dir) / f"session_{self.session_id}"
    
    def session_exists(self) -> bool:
        """Check if this session has existing persisted data.
        
        Returns:
            bool: True if session data exists on disk, False otherwise
        """
        session_path = self.get_session_path()
        session_file = session_path / "session.json"
        return session_file.exists()
