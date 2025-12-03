from typing import Dict, List


class PlanningAgent:
    def __init__(self, memory_service=None):
        """Initialize the Planning Agent with a memory service."""
        self.memory = memory_service


    def generate_daily_plan(self, profile: Dict, resources: List[Dict], day: int = 1) -> Dict:
        """Generate a daily plan based on the profile and resources."""
        daily_time = profile.get("daily_time", 0.5)
        task_base = max(1, int(daily_time * 2))
        plan = {
            "type": "learning_plan",
            "day": day,
            "tasks": [
                {"task": "Theory reading", "duration_min": int(daily_time*20)},
                {"task": "Mini-quiz", "duration_min": int(daily_time*10)},
                {"task": "Small coding exercise", "duration_min": int(daily_time*20)} ],
            "resources": resources[:3]
        }
        if self.memory:
            self.memory.append_daily_plan(plan)
        return plan