"""Streamlit frontend entry point for Edge Operator Agent.

Run with: streamlit run streamlit_app.py

Provides a web-based chat interface for interacting with the Edge Operator Agent,
with controls for switching between local and cloud model modes.

Requirements:
    - 8.1: Show slider/toggle control for selecting between Local and Cloud modes
    - 6.4: Provide coherent natural language response display
    - 5.6: Support document indexing through file upload
"""

import streamlit as st
from pathlib import Path
import tempfile
import os
import sys

# Add the e2e-demo directory to path so we can import src as a package
app_dir = Path(__file__).parent.absolute()
if str(app_dir) not in sys.path:
    sys.path.insert(0, str(app_dir))

from src.config import EdgeAgentConfig
from src.edge_operator_agent import EdgeOperatorAgent


def init_session_state():
    """Initialize Streamlit session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "agent" not in st.session_state:
        st.session_state.agent = None
    
    if "model_mode" not in st.session_state:
        st.session_state.model_mode = "local"
    
    if "session_id" not in st.session_state:
        st.session_state.session_id = "edge-operator-001"
    
    if "indexed_documents" not in st.session_state:
        st.session_state.indexed_documents = []


def get_agent() -> EdgeOperatorAgent:
    """Get or create the EdgeOperatorAgent instance.
    
    Returns:
        EdgeOperatorAgent: The agent instance from session state
    """
    if st.session_state.agent is None:
        config = EdgeAgentConfig(
            session_id=st.session_state.session_id,
            sessions_dir="./edge_sessions",
            db_path="./edge_telemetry.db",
            vector_store_path="./edge_vector_store",
            documents_dir="./edge_documents"
        )
        st.session_state.agent = EdgeOperatorAgent(config)
    
    return st.session_state.agent


def render_sidebar():
    """Render the sidebar with model mode toggle and status.
    
    Requirements:
        - 8.1: Show slider/toggle control for selecting between Local and Cloud modes
        - 8.5: Display error and remain in local mode if cloud unavailable
    """
    with st.sidebar:
        st.title("⚙️ Settings")
        
        st.markdown("---")
        
        # Model Mode Toggle (Requirement 8.1)
        st.subheader("🤖 Model Mode")
        
        mode_options = ["Local (Ollama)", "Cloud (Bedrock)"]
        current_index = 0 if st.session_state.model_mode == "local" else 1
        
        selected_mode = st.radio(
            "Select inference mode:",
            mode_options,
            index=current_index,
            help="Local mode uses Ollama for offline operation. Cloud mode uses Claude on Amazon Bedrock."
        )
        
        # Handle mode change
        new_mode = "local" if selected_mode == "Local (Ollama)" else "cloud"
        
        if new_mode != st.session_state.model_mode:
            agent = get_agent()
            success, message = agent.set_model_mode(new_mode)
            
            if success:
                st.session_state.model_mode = new_mode
                st.success(f"✅ {message}")
            else:
                # Requirement 8.5: Display error and remain in local mode
                st.error(f"❌ {message}")
                st.session_state.model_mode = "local"
        
        # Display current mode status
        st.markdown("---")
        st.subheader("📊 Status")
        
        mode_emoji = "🏠" if st.session_state.model_mode == "local" else "☁️"
        mode_label = "Local (Ollama)" if st.session_state.model_mode == "local" else "Cloud (Bedrock)"
        
        st.info(f"{mode_emoji} Current Mode: **{mode_label}**")
        
        # Session info
        st.markdown(f"📝 Session: `{st.session_state.session_id}`")
        
        st.markdown("---")
        
        # Document Management Section (Requirement 5.6)
        render_document_management()


def render_document_management():
    """Render document management UI in sidebar.
    
    Requirements:
        - 5.6: Support document indexing through file upload
    """
    st.subheader("📚 Documents")
    
    # File upload for document indexing
    uploaded_file = st.file_uploader(
        "Upload document to index",
        type=["txt", "md", "pdf"],
        help="Upload technical documents, manuals, or guides for semantic search"
    )
    
    if uploaded_file is not None:
        # Save uploaded file temporarily and index it
        with tempfile.NamedTemporaryFile(
            delete=False, 
            suffix=Path(uploaded_file.name).suffix
        ) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
        
        try:
            agent = get_agent()
            result = agent.doc_search.index_document(tmp_path)
            
            if "Successfully" in result:
                st.success(f"✅ Indexed: {uploaded_file.name}")
                if uploaded_file.name not in st.session_state.indexed_documents:
                    st.session_state.indexed_documents.append(uploaded_file.name)
            else:
                st.error(f"❌ {result}")
        finally:
            # Clean up temp file
            os.unlink(tmp_path)
    
    # Display indexed documents list
    if st.session_state.indexed_documents:
        st.markdown("**Indexed Documents:**")
        for doc in st.session_state.indexed_documents:
            st.markdown(f"- 📄 {doc}")
    else:
        st.caption("No documents indexed yet")


def stream_agent_response(agent: EdgeOperatorAgent, prompt: str):
    """Generator that yields text chunks from the agent's streaming response.
    
    Args:
        agent: The EdgeOperatorAgent instance
        prompt: The user's input message
        
    Yields:
        Text chunks as they are generated by the agent
    """
    import asyncio
    import threading
    import queue
    
    text_queue = queue.Queue()
    done_event = threading.Event()
    error_holder = [None]  # Use list to allow modification in nested function
    
    async def async_stream():
        """Async function to stream events and put text in queue."""
        try:
            async for text in agent.stream_chat(prompt):
                text_queue.put(text)
        except Exception as e:
            error_holder[0] = str(e)
        finally:
            done_event.set()
    
    def run_async():
        """Run the async stream in a new event loop."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(async_stream())
        finally:
            loop.close()
    
    # Start async streaming in background thread
    thread = threading.Thread(target=run_async, daemon=True)
    thread.start()
    
    # Yield chunks as they arrive
    while not done_event.is_set() or not text_queue.empty():
        try:
            chunk = text_queue.get(timeout=0.1)
            yield chunk
        except queue.Empty:
            continue
    
    thread.join(timeout=1.0)
    
    # If there was an error, yield it
    if error_holder[0]:
        yield f"\n\nError: {error_holder[0]}"


def render_chat_interface():
    """Render the main chat interface.
    
    Requirements:
        - 6.4: Provide coherent natural language response display
    """
    st.title("🏭 Edge Operator Agent")
    st.caption("AI-powered assistant for industrial equipment management")
    
    # Display chat messages
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        
        with st.chat_message(role):
            st.markdown(content)
    
    # Chat input
    if prompt := st.chat_input("Ask about sensors, equipment, or search documents..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get agent response with streaming
        with st.chat_message("assistant"):
            agent = get_agent()
            
            # Use st.write_stream for streaming response
            response = st.write_stream(stream_agent_response(agent, prompt))
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})


def main():
    """Main entry point for the Streamlit app."""
    # Page configuration
    st.set_page_config(
        page_title="Edge Operator Agent",
        page_icon="🏭",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    init_session_state()
    
    # Render sidebar with settings
    render_sidebar()
    
    # Render main chat interface
    render_chat_interface()


if __name__ == "__main__":
    main()
