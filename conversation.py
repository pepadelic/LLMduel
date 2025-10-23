"""Conversation Orchestration Module
Manages the dialogue flow between two LLM models.
"""

from typing import List, Dict, Optional
from llm_client import LLMClient
import os


class ConversationOrchestrator:
    """Orchestrates conversation between two LLM models."""
    
    def __init__(
        self,
        model_a_client: LLMClient,
        model_b_client: LLMClient,
        model_a_persona: str,
        model_b_persona: str,
        discussion_topic: str,
        temperature: float = 0.7,
        system_prompt_file: str = "system_prompt.txt"
    ):
        """
        Initialize conversation orchestrator.
        
        Args:
            model_a_client: LLM client for Model A
            model_b_client: LLM client for Model B
            model_a_persona: Persona description for Model A
            model_b_persona: Persona description for Model B
            discussion_topic: Topic of discussion
            temperature: Sampling temperature for responses
        """
        self.model_a_client = model_a_client
        self.model_b_client = model_b_client
        self.model_a_persona = model_a_persona
        self.model_b_persona = model_b_persona
        self.discussion_topic = discussion_topic
        self.temperature = temperature
        self.system_prompt_file = system_prompt_file
        
        # Store messages as they are exchanged
        self.messages: List[Dict[str, str]] = []
        
        # Load system prompt template
        self.system_prompt_template = self._load_system_prompt()
    
    def _load_system_prompt(self) -> str:
        """Load system prompt from file."""
        try:
            if os.path.exists(self.system_prompt_file):
                with open(self.system_prompt_file, 'r', encoding='utf-8') as f:
                    return f.read().strip()
            else:
                # Fallback to default prompt if file doesn't exist
                return (
                    "You are having a conversation with another AI assistant about: {topic}\n\n"
                    "Guidelines:\n"
                    "- Keep responses conversational and natural (2-4 sentences typically)\n"
                    "- Build on what the other assistant has said\n"
                    "- Feel free to ask questions, agree, disagree, or introduce new perspectives\n"
                    "- Stay on topic but allow the conversation to evolve naturally\n"
                    "- Be respectful and constructive in your dialogue"
                )
        except Exception as e:
            print(f"Warning: Could not load system prompt file: {e}")
            return "You are having a conversation with another AI assistant about: {topic}"
    
    def _build_context_for_model(
        self,
        persona: str,
        is_model_a: bool
    ) -> List[Dict[str, str]]:
        """
        Build conversation context for a specific model.
        
        Args:
            persona: The persona description for this model
            is_model_a: Whether this is Model A (True) or Model B (False)
        
        Returns:
            List of messages formatted for the API
        """
        # Start with system message
        # Combine persona with system prompt template
        system_prompt = self.system_prompt_template.format(topic=self.discussion_topic)
        system_message = {
            "role": "system",
            "content": f"{persona}\n\n{system_prompt}"
        }
        
        messages = [system_message]
        
        # If this is the very first message (Model A starting)
        if len(self.messages) == 0 and is_model_a:
            messages.append({
                "role": "user",
                "content": f"Please start a conversation about: {self.discussion_topic}. Share your initial thoughts on this topic in 2-4 sentences."
            })
        else:
            # Build conversation history with proper role alternation
            # The pattern must be: user → assistant → user → assistant
            # Each model sees the conversation from its own perspective
            
            for i, msg in enumerate(self.messages):
                # Determine which model sent this message
                # Turn 1 (index 0) = Model A, Turn 2 (index 1) = Model B, etc.
                msg_is_from_model_a = (i % 2 == 0)
                
                if msg_is_from_model_a == is_model_a:
                    # This is our own previous message - role is "assistant"
                    messages.append({
                        "role": "assistant",
                        "content": msg["content"]
                    })
                else:
                    # This is the other model's message - role is "user"
                    messages.append({
                        "role": "user",
                        "content": msg["content"]
                    })
            
            # Ensure we end with a user message to prompt the next response
            # Check the last message role
            if len(messages) > 1 and messages[-1]["role"] == "assistant":
                # We need to add a user prompt
                messages.append({
                    "role": "user",
                    "content": "Please continue the conversation."
                })
        
        return messages
    
    def get_next_response(self, turn_number: int) -> Dict[str, any]:
        """
        Get the next response in the conversation.
        
        Args:
            turn_number: Current turn number (1-indexed)
        
        Returns:
            Dictionary containing response data and metadata
        """
        # Determine which model should respond
        # Turn 1: Model A, Turn 2: Model B, Turn 3: Model A, etc.
        is_model_a_turn = (turn_number % 2 == 1)
        
        if is_model_a_turn:
            client = self.model_a_client
            persona = self.model_a_persona
            speaker = "Model A"
        else:
            client = self.model_b_client
            persona = self.model_b_persona
            speaker = "Model B"
        
        # Build context for this model
        context_messages = self._build_context_for_model(persona, is_model_a_turn)
        
        # Debug logging
        print(f"\n=== Turn {turn_number}: {speaker} ===")
        print(f"Messages sent to API:")
        for i, msg in enumerate(context_messages):
            content_preview = msg['content'][:60] + '...' if len(msg['content']) > 60 else msg['content']
            print(f"  {i}: {msg['role']}: {content_preview}")
        print()
        
        # Get response from the model
        result = client.generate_response(
            messages=context_messages,
            temperature=self.temperature
        )
        
        # If successful, add to message history
        if result['success']:
            self.messages.append({
                "content": result['content'],
                "speaker": speaker,
                "turn": turn_number
            })
        
        # Add speaker information to result
        result['speaker'] = speaker
        result['turn'] = turn_number
        
        return result
    
    def get_conversation_transcript(self) -> List[Dict[str, str]]:
        """
        Get the full conversation transcript.
        
        Returns:
            List of message dictionaries with speaker and content
        """
        return self.messages.copy()
    
    def reset(self):
        """Reset the conversation to initial state."""
        self.messages = []

