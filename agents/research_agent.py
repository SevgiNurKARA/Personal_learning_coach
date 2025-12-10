from typing import List, Dict


class ResearchAgent:
    def __init__(self, search_tool=None, memory_service=None):
        self.search_tool = search_tool
        self.memory = memory_service

    def build_query(self, profile: Dict) -> str:
        domain = profile.get("domain", "programming")
        level = profile.get("level", "beginner")
        return f"{level} {domain} tutorial best resources"

    def find_resources(self, profile: Dict) -> List[Dict]:
        query = self.build_query(profile)
        results = []
        if self.search_tool:
            results = self.search_tool.search(query, max_results=5)
        else:
            results = [{"title": "Intro to Python - Example Course", "url": "https://example.org/python"}, {"title": "Beginner Exercises", "url": "https://example.org/exercises"}]
        if self.memory:
            self.memory.save_recommendations(profile.get("goal"), results)
        return results