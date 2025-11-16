from typing import Dict, Any, List
import math
import os
import json
from datetime import datetime

def run_financial_model(assumptions: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simple financial model tool.

    Args:
        assumptions: dict with keys:
          - initial_users (int)
          - monthly_growth_rate (float, e.g. 0.1)
          - arpu (float)
          - fixed_costs (float)
          - variable_cost_per_user (float)
          - months (int, optional, default 36)

    Returns:
        dict with:
          - assumptions (echoed)
          - projections: list of {month, users, revenue, costs, profit}
          - break_even_month (int or null)
    """
    months = int(assumptions.get("months", 36))
    initial_users = float(assumptions.get("initial_users", 50))
    growth = float(assumptions.get("monthly_growth_rate", 0.1))
    arpu = float(assumptions.get("arpu", 5.0))
    fixed_costs = float(assumptions.get("fixed_costs", 1500.0))
    variable_cost_per_user = float(assumptions.get("variable_cost_per_user", 0.1))

    users = initial_users
    projections: List[Dict[str, Any]] = []
    break_even_month = None

    for month in range(1, months + 1):
        if month > 1:
            users *= (1.0 + growth)
        # Round users for presentation
        users_rounded = int(users)
        revenue = users_rounded * arpu
        costs = fixed_costs + users_rounded * variable_cost_per_user
        profit = revenue - costs

        projections.append(
            {
                "month": month,
                "users": users_rounded,
                "revenue": round(revenue, 2),
                "costs": round(costs, 2),
                "profit": round(profit, 2),
            }
        )

        if break_even_month is None and profit >= 0:
            break_even_month = month

    return {
        "assumptions": assumptions,
        "projections": projections,
        "break_even_month": break_even_month,
    }


def export_plan(plan_markdown: str, format: str = "markdown") -> Dict[str, Any]:
    """
    Export the generated plan to a local file (for demo purposes).

    This tool writes to a timestamped file in the current working directory.

    Args:
        plan_markdown: The plan content (Markdown or plain text).
        format: "markdown" or "text" (used for file extension only).

    Returns:
        dict with:
          - path: path to the saved file
          - format: format used
    """
    ext = "md" if format == "markdown" else "txt"
    ts = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    filename = f"business_plan_{ts}.{ext}"
    path = os.path.join(os.getcwd(), filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(plan_markdown)

    return {"path": path, "format": format}


def save_business_profile(profile_json: str) -> Dict[str, Any]:
    """
    Simple tool to acknowledge saving a structured business profile.

    In a real application, this might persist to a database or memory store.
    Here we just validate that it's valid JSON and echo it back.

    Args:
        profile_json: JSON string representing the business profile.

    Returns:
        dict with:
          - valid: bool
          - profile (parsed) or error
    """
    try:
        profile = json.loads(profile_json)
        return {"valid": True, "profile": profile}
    except Exception as e:
        return {"valid": False, "error": str(e)}
