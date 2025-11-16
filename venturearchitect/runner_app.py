import asyncio
import os

from dotenv import load_dotenv

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.plugins.logging_plugin import LoggingPlugin
from google.genai import types

from venturearchitect.agents.root_agent import venture_architect_root_agent

# Load environment variables from .env
load_dotenv()

#  IMPORTANT: ADK thinks the app name is "agents" (from the error path)
APP_NAME = "agents"


async def main() -> None:
    print("VentureArchitect – Business Plan Copilot")
    print("Describe your business idea in as much detail as you like.")
    print("You can paste a long, formal description (multiple paragraphs are welcome).\n")


    # Ensure API key is available
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY is not set. "
            "Add it to a .env file in the project root (GOOGLE_API_KEY=...) "
            "or export it in your environment."
        )

    user_idea = input("Enter a brief description of your business idea:\n> ").strip()
    if not user_idea:
        print("No idea entered. Exiting.")
        return

    # ---- Session + Runner setup ----
    session_service = InMemorySessionService()

    user_id = "cli_user"
    session_id = "cli_session"

    # CRITICAL: create the session BEFORE running the agent
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id,
    )

    # Optional: sanity check where the agent lives
    print(f"\nRoot agent module: {venture_architect_root_agent.__module__}")
    print(f"Using app_name: {APP_NAME}")
    print("\nGenerating your business plan (this may take a bit)...\n")

    # Create a Runner for the root agent
    runner = Runner(
        agent=venture_architect_root_agent,
        app_name=APP_NAME,
        session_service=session_service,
        plugins=[LoggingPlugin()],
    )

    # Build the Content object for the user message
    new_message = types.Content(parts=[types.Part(text=user_idea)])

    final_text_chunks: list[str] = []

    # Stream all events from the agent run
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=new_message,
    ):
        # LoggingPlugin already shows internal logs.
        # Here we only care about the FINAL response from the root agent.
        if event.is_final_response() and event.content:
            for part in event.content.parts:
                if hasattr(part, "text") and part.text:
                    final_text_chunks.append(part.text)

    print("\n === GENERATED OUTPUT FROM ROOT AGENT ===\n")
    if final_text_chunks:
        print("\n".join(final_text_chunks))
    else:
        print("No final response content was produced. Check logs above for details.")


if __name__ == "__main__":
    asyncio.run(main())
