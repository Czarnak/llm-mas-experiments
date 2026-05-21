from crewai import Agent
from textwrap import dedent


class ReporterAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(
            role="Reporter",
            goal=dedent("""
                Collect and compile information from all specialized agents to generate a comprehensive report
                about the property and its surrounding area.
            """),
            backstory=dedent("""
                You are the reporter agent responsible for collecting information from all specialized agents
                and compiling it into a clear, actionable report for the customer.
            """),
            verbose=True,
            allow_delegation=False,
            **kwargs
        )