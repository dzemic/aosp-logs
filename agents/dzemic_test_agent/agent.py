from google.adk.agents import Agent

#
# make sure you have .env file with 
# GOOGLE_GENAI_USE_VERTEXAI=FALSE
# GOOGLE_API_KEY=<created with google studio ai>
#

root_agent = Agent(
    name="dzemic_test_agent",
    # https://ai.google.dev/gemini-api/docs/models
    model="gemini-2.0-flash",
    description="Greeting agent",
    instruction="""
    You are a helpful assistant that greets the user. 
    Ask for the user's name and greet them by name.
    """,
)