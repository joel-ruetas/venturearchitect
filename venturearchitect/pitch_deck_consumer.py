"""
Example consumer agent that uses the VentureArchitect root agent via A2A
to generate a pitch deck outline from an existing business plan.
"""

from google.adk.agents import LlmAgent
from google.adk.agents.remote_a2a_agent import (
    RemoteA2aAgent,
    AGENT_CARD_WELL_KNOWN_PATH,
)
from google.adk.models.google_llm import Gemini
from google.genai import types
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
import asyncio

# Remote A2A proxy to VentureArchitect (assumes a2a_server is running on localhost:8001)
venture_architect_remote = RemoteA2aAgent(
    name="venture_architect_root_agent",
    description="Remote VentureArchitect multi-agent business plan generator.",
    agent_card=f"http://localhost:8001{AGENT_CARD_WELL_KNOWN_PATH}",
)

pitch_deck_agent = LlmAgent(
    name="pitch_deck_agent",
    model=Gemini(model="gemini-2.5-flash-lite"),
    description="Generates pitch deck outlines by calling VentureArchitect as a sub-agent.",
    instruction="""
You are a pitch deck generator agent.

You should:
1. Call the remote VentureArchitect agent to generate or update a business plan.
2. Convert the resulting plan into an outline for a slide deck:

Slides:
1. Title & Vision
2. Problem
3. Solution
4. Market & Customers
5. Business Model
6. Go-to-Market
7. Financial Highlights
8. Team & Roadmap
9. Risks & Mitigations
10. Call to Action

Your final response should present the slides as numbered headings with bullet points.
""",
    sub_agents=[venture_architect_remote],
)


async def demo_pitch_deck() -> None:
    session_service = InMemorySessionService()
    runner = Runner(
        agent=pitch_deck_agent,
        app_name="pitch_deck_app",
        session_service=session_service,
    )

    user_id = "demo_user"
    session_id = "pitch_session_1"

    user_message = types.Content(
        parts=[
            types.Part(
                text="Generate a pitch deck for a mobile app that helps homeowners discover local garage sales."
            )
        ]
    )

    print("Generating pitch deck outline via A2A...\n")

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=user_message,
    ):
        if event.is_final_response() and event.content:
            for part in event.content.parts:
                if hasattr(part, "text") and part.text:
                    print(part.text)


if __name__ == "__main__":
    asyncio.run(demo_pitch_deck())
