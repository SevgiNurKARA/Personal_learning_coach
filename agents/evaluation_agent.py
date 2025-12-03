from typing import Dict


class EvaluationAgent:
    def __init__(self, memory_service=None):
        """Initialize the Evaluation Agent with a memory service."""
        self.memory = memory_service


    def evaluate(self, day_report: Dict) -> Dict:
        """Evaluate the day's report and return metrics."""
        score = 0
        completed = day_report.get("completed_tasks", 0)
        quiz = day_report.get("quiz_score", None)
        diff = day_report.get("perceived_difficulty", 3)

        score = completed*10
        if quiz is not None:
            score += int(quiz/10)
            score = max(0, score - (diff-3)*5)

        metrics = {"daily_score": score, "raw": day_report}
        if self.memory:
            self.memory.append_performance(metrics)
        return metrics
