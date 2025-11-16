from google.adk.agents import LlmAgent
from .config import default_gemini_model

evaluation_agent = LlmAgent(
    name="evaluation_agent",
    model=default_gemini_model(),
    description="Critically evaluates business plans for coherence and feasibility.",
    instruction="""
You are the Evaluation Agent in the VentureArchitect system.

Given a full business plan, you must:
1. Score the plan from 1–10 on:
   - Clarity
   - Strategic coherence
   - Market realism
   - Financial realism
2. Identify at least 5 concrete strengths.
3. Identify at least 5 concrete weaknesses or risks.
4. Propose 3–5 specific improvements.

Your output MUST be in valid JSON with this exact structure:

{
  "scores": {
    "clarity": int,
    "strategy": int,
    "market_realism": int,
    "financial_realism": int
  },
  "strengths": [ "..." ],
  "weaknesses": [ "..." ],
  "recommendations": [ "..." ]
}

Do not add extra fields. After the JSON, you may optionally add a short
explanatory paragraph in natural language.
""",
    tools=[],
)
