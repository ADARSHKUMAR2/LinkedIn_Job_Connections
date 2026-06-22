import os
import sys
from dotenv import load_dotenv
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

# Load environment configuration variables
load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))

class GitHubModelConfig:
    """Central configuration store for GitHub Models endpoints."""
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    ENDPOINT = "https://models.inference.ai.azure.com"
    
    # Model Router Definitions (Swap these values out to instantly update models globally)
    DEFAULT_MODEL = "gpt-4o"
    REASONING_MODEL = "o1-mini"  
    MINI_MODEL = "gpt-4o-mini"

def get_chat_inference_client() -> ChatCompletionsClient:
    """
    Factory function that builds and returns an authenticated 
    GitHub Models ChatCompletionsClient instance.
    """
    if not GitHubModelConfig.GITHUB_TOKEN:
        print(
            "⚠️  AI CLIENT CONFIG WARNING: 'GITHUB_TOKEN' is missing from your environment variables.\n"
            "   Please add it to your .env file to enable semantic LLM features.",
            file=sys.stderr
        )
        return None
        
    return ChatCompletionsClient(
        endpoint=GitHubModelConfig.ENDPOINT,
        credential=AzureKeyCredential(GitHubModelConfig.GITHUB_TOKEN)
    )