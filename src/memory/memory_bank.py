import json
from pathlib import Path
from typing import Any, Dict, List


class MemoryBank:
    def __init__(self, path: str = "data/memory/user_profile_store.json"):
        """Initialize the Memory Bank with a path to the user profile store."""
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write({"user_profile": {}, "recommendations": [], "daily_plans": [], "performance": []})

    def _read(self) -> Dict[str, Any]:
        """Read the memory bank from the file."""
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, payload: Dict[str, Any]):
        """Write the memory bank to the file."""
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

    def save_user_profile(self, profile: Dict[str, Any]):
        data = self._read()
        data["user_profile"] = profile
        self._write(data)

    def get_user_profile(self) -> Dict[str, Any]:
        """Get the user profile from the memory bank."""
        return self._read().get("user_profile", {})

    def save_recommendations(self, key: str, recs: List[Dict[str, Any]]):
        """Save the recommendations to the memory bank."""
        data = self._read()
        data.setdefault("recommendations", []).append({"key": key, "recs": recs})
        self._write(data)

    def append_daily_plan(self, plan: Dict[str, Any]):
        """Append the daily plan to the memory bank."""
        data = self._read()
        data.setdefault("daily_plans", []).append(plan)
        self._write(data)

    def append_performance(self, metrics: Dict[str, Any]):
        """Append the performance metrics to the memory bank."""
        data = self._read()
        data.setdefault("performance", []).append(metrics)
        self._write(data)