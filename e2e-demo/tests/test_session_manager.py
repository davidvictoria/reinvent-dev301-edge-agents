"""Tests for session management functionality.

Verifies that the session manager correctly creates directories,
persists sessions, and integrates with the agent.
"""

import os
import tempfile
import shutil
from pathlib import Path

import pytest

from src.session_manager import create_session_manager, EdgeSessionManager


class TestCreateSessionManager:
    """Tests for the create_session_manager function."""
    
    def test_creates_storage_directory(self):
        """Test that storage directory is created if it doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage_dir = os.path.join(tmpdir, "new_sessions")
            
            # Directory should not exist yet
            assert not os.path.exists(storage_dir)
            
            # Create session manager
            session_manager = create_session_manager(
                session_id="test-session",
                storage_dir=storage_dir
            )
            
            # Directory should now exist
            assert os.path.exists(storage_dir)
            assert os.path.isdir(storage_dir)
    
    def test_creates_nested_directories(self):
        """Test that nested directory paths are created."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage_dir = os.path.join(tmpdir, "level1", "level2", "sessions")
            
            session_manager = create_session_manager(
                session_id="nested-test",
                storage_dir=storage_dir
            )
            
            assert os.path.exists(storage_dir)
    
    def test_returns_file_session_manager(self):
        """Test that a FileSessionManager instance is returned."""
        from strands.session.file_session_manager import FileSessionManager
        
        with tempfile.TemporaryDirectory() as tmpdir:
            session_manager = create_session_manager(
                session_id="type-test",
                storage_dir=tmpdir
            )
            
            assert isinstance(session_manager, FileSessionManager)


class TestEdgeSessionManager:
    """Tests for the EdgeSessionManager class."""
    
    def test_lazy_initialization(self):
        """Test that session manager is lazily initialized."""
        with tempfile.TemporaryDirectory() as tmpdir:
            edge_manager = EdgeSessionManager(
                session_id="lazy-test",
                storage_dir=tmpdir
            )
            
            # Internal session manager should be None initially
            assert edge_manager._session_manager is None
            
            # Accessing the property should initialize it
            _ = edge_manager.session_manager
            assert edge_manager._session_manager is not None
    
    def test_get_session_path(self):
        """Test that session path is correctly computed."""
        with tempfile.TemporaryDirectory() as tmpdir:
            edge_manager = EdgeSessionManager(
                session_id="path-test",
                storage_dir=tmpdir
            )
            
            expected_path = Path(tmpdir) / "session_path-test"
            assert edge_manager.get_session_path() == expected_path
    
    def test_session_exists_false_for_new_session(self):
        """Test that session_exists returns False for new sessions."""
        with tempfile.TemporaryDirectory() as tmpdir:
            edge_manager = EdgeSessionManager(
                session_id="new-session",
                storage_dir=tmpdir
            )
            
            assert edge_manager.session_exists() is False
    
    def test_session_isolation(self):
        """Test that different session IDs have different paths."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager1 = EdgeSessionManager(session_id="session-1", storage_dir=tmpdir)
            manager2 = EdgeSessionManager(session_id="session-2", storage_dir=tmpdir)
            
            # Paths should be different
            assert manager1.get_session_path() != manager2.get_session_path()
            
            # Both should be in the same parent directory
            assert manager1.get_session_path().parent == manager2.get_session_path().parent
