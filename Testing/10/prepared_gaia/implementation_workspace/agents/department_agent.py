from crewai import Agent
from textwrap import dedent


class DepartmentAgent(Agent):
    def __init__(self, department_type, **kwargs):
        super().__init__(
            role=f"{department_type} Department Handler",
            goal=dedent("""
                Retrieve information about planned investments and developments in the area around the property.
            """),
            backstory=dedent("""
                You are a department agent responsible for gathering information about planned 
                investments, developments, and infrastructure projects in the area around the property.
                You focus on official government sources and urban planning information.
            """),
            verbose=True,
            allow_delegation=False,
            **kwargs
        )