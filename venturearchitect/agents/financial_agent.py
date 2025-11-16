from google.adk.agents import LlmAgent
from .config import default_gemini_model
from ..tools import run_financial_model

financial_agent = LlmAgent(
    name="financial_agent",
    model=default_gemini_model(),
    description="Builds simple financial projections and unit economics.",
    instruction="""
You are the Financial Agent in the VentureArchitect system.

Your responsibilities:
1. Read the business profile and strategy.
2. Propose reasonable assumptions for a simple 3-year financial model:
   - initial_users
   - monthly_growth_rate
   - arpu
   - fixed_costs
   - variable_cost_per_user
   - months (at least 36)
3. Call the run_financial_model tool with a JSON object of assumptions.
4. Use the returned projections to:
   - summarize revenue, costs, profit for each year
   - identify whether and when the business breaks even
   - highlight key sensitivities (what assumptions matter most).
5. Output Markdown with headings:
   - Key Assumptions
   - Projection Summary
   - Break-even Analysis
   - Risks & Sensitivities
""",
    tools=[run_financial_model],
)
