from .profile_agent import ProfileAgent
from .research_agent import ResearchAgent
from .planning_agent import PlanningAgent
from .evaluation_agent import EvaluationAgent


class OrchestratorAgent:
    def __init__(self, search_tool=None, memory_service=None):
        """Initialize the Orchestrator Agent with a search tool and a memory service."""
        self.memory = memory_service
        self.profile_agent = ProfileAgent(memory_service=memory_service)
        self.research_agent = ResearchAgent(search_tool=search_tool, memory_service=memory_service)
        self.planning_agent = PlanningAgent(memory_service=memory_service)
        self.evaluation_agent = EvaluationAgent(memory_service=memory_service)

    def run_initial_flow(self, user_input: dict):
        """Run the initial flow of the Orchestrator Agent."""
        if self.memory:
            profile = self.profile_agent.analyze(user_input)
        else:
            profile = {}
        if self.memory:
            resources = self.research_agent.find_resources(profile)
        else:
            resources = []
        if self.memory:
            plan = self.planning_agent.generate_daily_plan(profile, resources, day=1)
        else:
            plan = {}
        return {"profile": profile, "plan": plan, "resources": resources}

    def run_daily_cycle(self, user_id: str, day_report: dict):
        """Run the daily cycle of the Orchestrator Agent."""
        if self.memory:
            eval_metrics = self.evaluation_agent.evaluate(day_report)
        else:
            eval_metrics = {}
        if self.memory:
            profile = self.memory.get_user_profile()
        else:
            profile = {}
        resources = self.research_agent.find_resources(profile)
        next_plan = self.planning_agent.generate_daily_plan(profile, resources, day=day_report.get("day", 1)+1)
        return {"evaluation": eval_metrics, "next_plan": next_plan}
