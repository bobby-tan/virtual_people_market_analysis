from agentfield import Agent, AIConfig
from reasoners import reasoners_router
import os
from dotenv import load_dotenv
load_dotenv()

# Basic agent setup - works immediately
app = Agent(
    node_id="my-agent",
    agentfield_server="http://localhost:8080",
    version="1.0.0",
    dev_mode=True,

    # 🔧 Uncomment to enable AI features:
    ai_config=AIConfig(
        model="gemini/gemini-2.5-flash",  # LiteLLM auto-detects provider from model name
        api_key=os.getenv("GEMINI_API_KEY"),  # or set OPENAI_API_KEY env var
        temperature=0.7,
        max_tokens=4096,
    ),
)

# Include reasoners from separate file
app.include_router(reasoners_router)

if __name__ == "__main__":
    # Auto-discover available port starting from 8000
    app.serve(auto_port=True, dev=True, reload=False)
