"""
LLM API Client Module
Handles communication with LLM endpoints using OpenAI-compatible API format.
"""

from openai import OpenAI
from typing import List, Dict, Optional
import time


class LLMClient:
    """Client for interacting with LLM APIs."""
    
    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        model: str = "gpt-4.1-mini",
        timeout: int = 60
    ):
        """
        Initialize LLM client.
        
        Args:
            api_key: API key for authentication
            base_url: Base URL for the API endpoint (optional)
            model: Model name to use
            timeout: Request timeout in seconds
        """
        self.model = model
        self.timeout = timeout
        
        # Initialize OpenAI client
        if base_url:
            self.client = OpenAI(api_key=api_key, base_url=base_url)
        else:
            self.client = OpenAI(api_key=api_key)
    
    def generate_response(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> Dict[str, any]:
        """
        Generate a response from the LLM.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Sampling temperature (0.0 to 2.0)
            max_tokens: Maximum tokens to generate (optional)
        
        Returns:
            Dictionary containing response data and metadata
        """
        try:
            start_time = time.time()
            
            # Make API call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=self.timeout
            )
            
            elapsed_time = time.time() - start_time
            
            # Extract response content
            content = response.choices[0].message.content
            finish_reason = response.choices[0].finish_reason
            
            # Extract token usage if available
            usage = None
            if hasattr(response, 'usage') and response.usage:
                usage = {
                    'prompt_tokens': response.usage.prompt_tokens,
                    'completion_tokens': response.usage.completion_tokens,
                    'total_tokens': response.usage.total_tokens
                }
            
            return {
                'success': True,
                'content': content,
                'finish_reason': finish_reason,
                'usage': usage,
                'elapsed_time': elapsed_time,
                'error': None
            }
            
        except Exception as e:
            return {
                'success': False,
                'content': None,
                'finish_reason': None,
                'usage': None,
                'elapsed_time': None,
                'error': str(e)
            }
    
    def test_connection(self) -> Dict[str, any]:
        """
        Test the connection to the LLM API.
        
        Returns:
            Dictionary with success status and error message if any
        """
        try:
            # Simple test message
            test_messages = [
                {"role": "user", "content": "Hello"}
            ]
            
            result = self.generate_response(test_messages, max_tokens=10)
            
            if result['success']:
                return {'success': True, 'error': None}
            else:
                return {'success': False, 'error': result['error']}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}

