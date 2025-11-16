"""
business_plan_agent package

This is a thin wrapper so tools (or your own code) can do:

    import business_plan_agent
    business_plan_agent.root_agent

The actual agent lives in agent.py.
"""

from .agent import root_agent

__all__ = ["root_agent"]
