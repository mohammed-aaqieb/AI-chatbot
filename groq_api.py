# groq_api.py
from groq import Groq
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace with your actual Groq API key
GROQ_API_KEY = "your_api_key_here"

def get_groq_response(messages, model="llama-3.1-8b-instant"):
    """
    Get response from Groq API
    """
    try:
        # Initialize Groq client
        client = Groq(api_key=GROQ_API_KEY)
        
        # Create chat completion
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=model,
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )
        
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        logger.error(f"Error calling Groq API: {str(e)}")
        raise Exception(f"API call failed: {str(e)}")