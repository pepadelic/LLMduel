"""
LLM Conversation App - Main Application
An interactive Streamlit app where two LLMs hold a conversation with each other.
"""

import streamlit as st
from llm_client import LLMClient
from conversation import ConversationOrchestrator
from config import Config
from datetime import datetime
import json
import os
import time


# Page configuration
st.set_page_config(
    page_title="LLM Duel",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
)


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    
    if 'is_running' not in st.session_state:
        st.session_state.is_running = False
    
    if 'current_turn' not in st.session_state:
        st.session_state.current_turn = 0
    
    if 'model_a_client' not in st.session_state:
        st.session_state.model_a_client = None
    
    if 'model_b_client' not in st.session_state:
        st.session_state.model_b_client = None
    
    if 'config' not in st.session_state:
        st.session_state.config = {}
    
    if 'stop_requested' not in st.session_state:
        st.session_state.stop_requested = False
    
    if 'orchestrator' not in st.session_state:
        st.session_state.orchestrator = None


def render_sidebar():
    """Render the configuration sidebar."""
    st.sidebar.title("⚙️ Configuration")
    
    # Add checkbox to use same model for both personas
    use_same_model = st.sidebar.checkbox(
        "Use same model for both personas",
        value=False,
        key="use_same_model",
        help="When checked, Model B will use Model A's API settings"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("Model A Configuration")
    
    model_a_api_key = st.sidebar.text_input(
        "API Key (Model A)",
        type="password",
        value=Config.MODEL_A_API_KEY,
        key="model_a_api_key",
        help="Leave empty to use .env configuration"
    )
    
    model_a_base_url = st.sidebar.text_input(
        "Base URL (Model A) - Optional",
        value=Config.MODEL_A_BASE_URL or "",
        key="model_a_base_url",
        help="Leave empty to use default OpenAI endpoint or .env configuration"
    )
    
    model_a_name = st.sidebar.text_input(
        "Model Name (Model A)",
        value=Config.MODEL_A_NAME,
        key="model_a_name"
    )
    
    model_a_nickname = st.sidebar.text_input(
        "Nickname (Model A)",
        value=Config.MODEL_A_NICKNAME,
        key="model_a_nickname",
        help="Display name in conversation"
    )
    
    model_a_persona = st.sidebar.text_area(
        "Persona/Behavior (Model A)",
        value=Config.MODEL_A_PERSONA,
        key="model_a_persona",
        height=100
    )
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("Model B Configuration")
    
    model_b_api_key = st.sidebar.text_input(
        "API Key (Model B)",
        type="password",
        value=Config.MODEL_B_API_KEY if not use_same_model else Config.MODEL_A_API_KEY,
        key="model_b_api_key",
        disabled=use_same_model,
        help="Leave empty to use .env configuration"
    )
    
    model_b_base_url = st.sidebar.text_input(
        "Base URL (Model B) - Optional",
        value=Config.MODEL_B_BASE_URL or "",
        key="model_b_base_url",
        disabled=use_same_model,
        help="Leave empty to use default OpenAI endpoint or .env configuration"
    )
    
    model_b_name = st.sidebar.text_input(
        "Model Name (Model B)",
        value=Config.MODEL_B_NAME if not use_same_model else Config.MODEL_A_NAME,
        key="model_b_name",
        disabled=use_same_model
    )
    
    model_b_nickname = st.sidebar.text_input(
        "Nickname (Model B)",
        value=Config.MODEL_B_NICKNAME,
        key="model_b_nickname",
        help="Display name in conversation"
    )
    
    model_b_persona = st.sidebar.text_area(
        "Persona/Behavior (Model B)",
        value=Config.MODEL_B_PERSONA,
        key="model_b_persona",
        height=100
    )
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("Conversation Settings")
    
    discussion_topic = st.sidebar.text_area(
        "Discussion Topic",
        value=Config.DISCUSSION_TOPIC,
        key="discussion_topic",
        height=80
    )
    
    max_turns = st.sidebar.slider(
        "Maximum Turns",
        min_value=2,
        max_value=50,
        value=Config.MAX_TURNS,
        key="max_turns",
        help="Total number of exchanges (each model speaks once per turn)"
    )
    
    temperature = st.sidebar.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=Config.TEMPERATURE,
        step=0.1,
        key="temperature",
        help="Higher values make output more random, lower values more deterministic"
    )
    
    turn_delay = st.sidebar.slider(
        "Turn Delay (seconds)",
        min_value=0.0,
        max_value=5.0,
        value=Config.TURN_DELAY,
        step=0.5,
        key="turn_delay",
        help="Delay between turns to prevent rate limiting"
    )
    
    # Store configuration
    # If use_same_model is checked, copy Model A settings to Model B
    if use_same_model:
        model_b_api_key = model_a_api_key
        model_b_base_url = model_a_base_url
        model_b_name = model_a_name
    
    st.session_state.config = {
        'model_a': {
            'api_key': model_a_api_key,
            'base_url': model_a_base_url if model_a_base_url else None,
            'name': model_a_name,
            'nickname': model_a_nickname,
            'persona': model_a_persona
        },
        'model_b': {
            'api_key': model_b_api_key,
            'base_url': model_b_base_url if model_b_base_url else None,
            'name': model_b_name,
            'nickname': model_b_nickname,
            'persona': model_b_persona
        },
        'discussion_topic': discussion_topic,
        'max_turns': max_turns,
        'temperature': temperature,
        'turn_delay': turn_delay
    }
    
    return st.session_state.config


def validate_configuration(config):
    """
    Validate user configuration.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not config['model_a']['api_key']:
        return False, "Model A API key is required"
    
    if not config['model_b']['api_key']:
        return False, "Model B API key is required"
    
    if not config['model_a']['name']:
        return False, "Model A name is required"
    
    if not config['model_b']['name']:
        return False, "Model B name is required"
    
    if not config['discussion_topic']:
        return False, "Discussion topic is required"
    
    return True, None


def initialize_clients(config):
    """Initialize LLM clients for both models."""
    try:
        # Initialize Model A client
        st.session_state.model_a_client = LLMClient(
            api_key=config['model_a']['api_key'],
            base_url=config['model_a']['base_url'],
            model=config['model_a']['name']
        )
        
        # Initialize Model B client
        st.session_state.model_b_client = LLMClient(
            api_key=config['model_b']['api_key'],
            base_url=config['model_b']['base_url'],
            model=config['model_b']['name']
        )
        
        return True, None
    except Exception as e:
        return False, f"Failed to initialize clients: {str(e)}"


def generate_markdown_transcript(conversation_history, config):
    """Generate a Markdown-formatted transcript of the conversation."""
    lines = []
    lines.append("# LLM Conversation Transcript")
    lines.append("")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("## Configuration")
    lines.append("")
    lines.append(f"**Discussion Topic:** {config['discussion_topic']}")
    lines.append("")
    lines.append(f"**Model A:** {config['model_a']['name']}")
    lines.append(f"- Persona: {config['model_a']['persona']}")
    lines.append("")
    lines.append(f"**Model B:** {config['model_b']['name']}")
    lines.append(f"- Persona: {config['model_b']['persona']}")
    lines.append("")
    lines.append(f"**Temperature:** {config['temperature']}")
    lines.append(f"**Max Turns:** {config['max_turns']}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Conversation")
    lines.append("")
    
    for msg in conversation_history:
        speaker = msg['speaker']
        content = msg['content']
        turn = msg.get('turn', 0)
        timestamp = msg.get('timestamp', '')
        
        lines.append(f"### Turn {turn}: {speaker}")
        if timestamp:
            lines.append(f"*{timestamp}*")
        lines.append("")
        lines.append(content)
        lines.append("")
        lines.append("---")
        lines.append("")
    
    # Add statistics
    lines.append("## Statistics")
    lines.append("")
    lines.append(f"- **Total Turns:** {len(conversation_history)}")
    model_a_count = sum(1 for msg in conversation_history if msg['speaker'] == 'Model A')
    model_b_count = sum(1 for msg in conversation_history if msg['speaker'] == 'Model B')
    lines.append(f"- **Model A Messages:** {model_a_count}")
    lines.append(f"- **Model B Messages:** {model_b_count}")
    
    # Calculate average response times if available
    response_times = [msg.get('elapsed_time') for msg in conversation_history if msg.get('elapsed_time')]
    if response_times:
        avg_time = sum(response_times) / len(response_times)
        lines.append(f"- **Average Response Time:** {avg_time:.2f}s")
    
    return "\n".join(lines)


def render_conversation():
    """Render the conversation history with visual distinction between speakers."""
    conversation_container = st.container()
    
    # Get nicknames from config
    config = st.session_state.config
    nickname_a = config.get('model_a', {}).get('nickname', 'Model A')
    nickname_b = config.get('model_b', {}).get('nickname', 'Model B')
    
    with conversation_container:
        for msg in st.session_state.conversation_history:
            speaker = msg['speaker']
            content = msg['content']
            turn = msg.get('turn', 0)
            
            # Create columns for alignment
            if speaker == 'Model A':
                col1, col2, col3 = st.columns([6, 1, 1])
                with col1:
                    st.markdown(
                        f"<div style='background-color: #e3f2fd; padding: 15px; border-radius: 10px; "
                        f"border-left: 5px solid #2196f3; margin-bottom: 10px;'>"
                        f"<strong style='color: #1976d2;'>🤖 {nickname_a}</strong> <span style='color: #666; font-size: 0.9em;'>(Turn {turn})</span><br>"
                        f"<span style='color: #333;'>{content}</span>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
            else:  # Model B
                col1, col2, col3 = st.columns([1, 1, 6])
                with col3:
                    st.markdown(
                        f"<div style='background-color: #f3e5f5; padding: 15px; border-radius: 10px; "
                        f"border-right: 5px solid #9c27b0; margin-bottom: 10px;'>"
                        f"<strong style='color: #7b1fa2;'>🤖 {nickname_b}</strong> <span style='color: #666; font-size: 0.9em;'>(Turn {turn})</span><br>"
                        f"<span style='color: #333;'>{content}</span>"
                        f"</div>",
                        unsafe_allow_html=True
                    )


def run_conversation(config):
    """Execute the conversation loop."""
    # Initialize orchestrator if not already done
    if st.session_state.orchestrator is None:
        st.session_state.orchestrator = ConversationOrchestrator(
            model_a_client=st.session_state.model_a_client,
            model_b_client=st.session_state.model_b_client,
            model_a_persona=config['model_a']['persona'],
            model_b_persona=config['model_b']['persona'],
            discussion_topic=config['discussion_topic'],
            temperature=config['temperature'],
            system_prompt_file=Config.SYSTEM_PROMPT_FILE
        )
    
    # Get next turn number
    next_turn = st.session_state.current_turn + 1
    max_turns = config['max_turns']
    
    # Check if conversation should continue
    if next_turn > max_turns or st.session_state.stop_requested:
        st.session_state.is_running = False
        if next_turn > max_turns:
            st.success(f"✅ Conversation completed! Reached maximum of {max_turns} turns.")
        else:
            st.warning("⏹️ Conversation stopped by user.")
        return
    
    # Show progress indicator with nickname (non-blocking)
    is_model_a = (next_turn % 2 == 1)
    nickname = config['model_a']['nickname'] if is_model_a else config['model_b']['nickname']
    
    # Create status container
    status_container = st.empty()
    status_container.info(f"🤔 {nickname} is thinking... (Turn {next_turn}/{max_turns})")
    
    # Get next response
    result = st.session_state.orchestrator.get_next_response(next_turn)
    
    # Clear status
    status_container.empty()
    
    if result['success']:
        # Add to conversation history
        st.session_state.conversation_history.append({
            'turn': result['turn'],
            'speaker': result['speaker'],
            'content': result['content'],
            'timestamp': datetime.now().isoformat(),
            'usage': result.get('usage'),
            'elapsed_time': result.get('elapsed_time')
        })
        
        # Update turn counter
        st.session_state.current_turn = next_turn
        
        # Configurable delay to prevent rate limiting
        time.sleep(config.get('turn_delay', 1.0))
        
        # Rerun to display new message and continue
        st.rerun()
    else:
        # Handle error
        st.error(f"❌ Error getting response from {result['speaker']}: {result['error']}")
        st.session_state.is_running = False
        st.session_state.stop_requested = True


def main():
    """Main application entry point."""
    initialize_session_state()
    
    # Render sidebar and get configuration
    config = render_sidebar()
    
    # Main area
    st.title("⚔️ LLM Duel")
    st.markdown("Watch two AI models engage in a real-time conversation on any topic you choose.")
    
    # Display conversation area
    st.markdown("---")
    
    # Control buttons
    col1, col2, col3, col4 = st.columns([1, 1, 1, 3])
    
    with col1:
        if not st.session_state.is_running:
            if st.button("▶️ Start Conversation", type="primary", use_container_width=True, key="start_btn"):
                # Validate configuration
                is_valid, error_msg = validate_configuration(config)
                if not is_valid:
                    st.error(f"Configuration Error: {error_msg}")
                else:
                    # Initialize clients
                    success, error_msg = initialize_clients(config)
                    if not success:
                        st.error(error_msg)
                    else:
                        # Reset conversation state
                        st.session_state.conversation_history = []
                        st.session_state.current_turn = 0
                        st.session_state.stop_requested = False
                        st.session_state.orchestrator = None
                        st.session_state.is_running = True
                        st.rerun()
    
    with col2:
        if st.session_state.is_running:
            if st.button("⏹️ Stop", type="secondary", use_container_width=True, key="stop_btn"):
                st.session_state.stop_requested = True
                st.session_state.is_running = False
                st.rerun()
    
    with col3:
        if st.session_state.conversation_history and not st.session_state.is_running:
            if st.button("🔄 New Conversation", type="secondary", use_container_width=True, key="new_btn"):
                # Reset conversation state
                st.session_state.conversation_history = []
                st.session_state.current_turn = 0
                st.session_state.stop_requested = False
                st.session_state.orchestrator = None
                st.rerun()
    
    # Display conversation or info message
    if st.session_state.conversation_history:
        st.markdown("### ⚔️ Conversation")
        render_conversation()
    elif not st.session_state.is_running:
        st.info("👆 Configure the models in the sidebar and click 'Start Conversation' to begin.")
    
    # Run conversation if active - MUST be after buttons
    if st.session_state.is_running:
        run_conversation(config)
    
    # Export transcript button
    if st.session_state.conversation_history and not st.session_state.is_running:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 4])
        
        with col1:
            # Export as JSON
            transcript_json = json.dumps(
                st.session_state.conversation_history,
                indent=2,
                ensure_ascii=False
            )
            st.download_button(
                label="📥 Download JSON",
                data=transcript_json,
                file_name=f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col2:
            # Export as Markdown
            transcript_md = generate_markdown_transcript(
                st.session_state.conversation_history,
                config
            )
            st.download_button(
                label="📥 Download Markdown",
                data=transcript_md,
                file_name=f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
                use_container_width=True
            )
    
    # Display conversation statistics
    if st.session_state.conversation_history:
        st.markdown("---")
        st.subheader("📊 Conversation Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Turns", st.session_state.current_turn)
        
        with col2:
            total_messages = len(st.session_state.conversation_history)
            st.metric("Total Messages", total_messages)
        
        with col3:
            model_a_messages = sum(1 for msg in st.session_state.conversation_history if msg['speaker'] == 'Model A')
            st.metric("Model A Messages", model_a_messages)
        
        with col4:
            model_b_messages = sum(1 for msg in st.session_state.conversation_history if msg['speaker'] == 'Model B')
            st.metric("Model B Messages", model_b_messages)


if __name__ == "__main__":
    main()

