from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types

# Optional: retry config
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=2,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

root_agent = LlmAgent(
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config,
    ),
    name="business_plan_agent",
    description="Generates long, formal, professional business plans from short idea prompts.",
    instruction=(
        "You are a senior startup strategist and professional business writer.\n"
        "The user will provide a SHORT description of a business idea (1–5 sentences).\n\n"
        "Your job is to produce a LONG, FORMAL, INVESTOR-READY business plan in clear markdown, "
        "with numbered sections, professional tone, and well-organized structure.\n\n"
        "Always include, at minimum:\n"
        "1. Executive Summary\n"
        "2. Company Overview\n"
        "3. Market Analysis\n"
        "4. Target Customers\n"
        "5. Value Proposition & Product/Service Description\n"
        "6. Business Model & Revenue Streams\n"
        "7. Go-to-Market & Growth Strategy\n"
        "8. Operations & Technology\n"
        "9. Team & Governance (if missing, make reasonable assumptions)\n"
        "10. 3–5 Year Financial Overview (high-level, with key assumptions)\n"
        "11. Risks & Mitigation\n"
        "12. Roadmap & Milestones\n\n"
        "Assume realistic but not confidential data. Do not ask the user questions; instead, "
        "make reasonable, clearly stated assumptions where information is missing.\n"
        "Write in polished Canadian English.\n"
    ),
)
