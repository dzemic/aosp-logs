from datetime import datetime

from google.adk.agents import Agent
from google.adk.tools import google_search


#
# make sure you have .env file with 
# GOOGLE_GENAI_USE_VERTEXAI=FALSE
# GOOGLE_API_KEY=<created with google studio ai>
#
# use google_search or get_current_time tool

def get_current_time() -> dict:
    """
    Get the current time in the format YYYY-MM-DD HH:MM:SS
    """
    return {
        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

root_agent = Agent(
    name="memory_agent",
    # https://ai.google.dev/gemini-api/docs/models
    model="gemini-2.0-flash",
    description="Rude agent",
    instruction="""
    You are very rude assistant use follwoing tools:
    - get_current_time
    """,
    tools=[get_current_time],
)