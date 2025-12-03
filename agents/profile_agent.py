from typing import Dict


class ProfileAgent:
    def __init__(self, memory_service=None):
        """Initialize the Profile Agent with a memory service."""
        self.memory = memory_service


    def analyze(self, user_input: Dict) -> Dict:
        """Analyze the user's input and return a profile."""
        profile = {
    "goal": user_input.get("goal"),
"level": user_input.get("current_level", "unknown"),
"daily_time": float(user_input.get("daily_available_time", 0)),
"style": user_input.get("preferred_learning_style", "balanced"),
"created_at": user_input.get("created_at")
}
        if "python" in (profile["goal"] or "").lower():
            profile["domain"] = "python"
        else:
            profile["domain"] = "general"

        if self.memory:
            self.memory.save_user_profile(profile)

        return profile