"""
Orchestrator Agent - Ana Koordinatör
====================================
Tüm agent'ları koordine eder ve veri akışını yönetir (Yeni 5-Agent Mimarisi).
"""

from .assessment_agent import get_assessment_agent
from .roadmap_agent import get_roadmap_agent
from .content_curator_agent import get_content_curator_agent
from .quiz_validation_agent import get_quiz_validation_agent
from .progress_agent import get_progress_agent


class OrchestratorAgent:
    """Agent'lar arası koordinasyonu sağlayan ana sınıf."""
    
    def __init__(self, search_tool=None, memory_service=None):
        """Initialize the Orchestrator Agent with all sub-agents."""
        self.memory = memory_service
        
        # 5 Temel Agent
        self.assessment_agent = get_assessment_agent()         # Agent 1
        self.roadmap_agent = get_roadmap_agent()               # Agent 2
        self.content_curator_agent = get_content_curator_agent() # Agent 3
        self.quiz_validation_agent = get_quiz_validation_agent() # Agent 4
        self.progress_agent = get_progress_agent()             # Agent 5
        
        # Servisleri agentlara enjekte et (gerekirse)
        if hasattr(self.assessment_agent, 'memory'):
            self.assessment_agent.memory = memory_service
        if hasattr(self.content_curator_agent, 'memory'):
            self.content_curator_agent.memory = memory_service
            self.content_curator_agent.search_tool = search_tool
        if hasattr(self.progress_agent, 'memory'):
            self.progress_agent.memory = memory_service

    def run_initial_flow(self, user_input: dict):
        """Başlangıç akışını çalıştırır: Profil Analizi -> Kaynaklar -> İlk Plan."""
        
        # 1. Profil Analizi (Assessment Agent)
        profile = self.assessment_agent.analyze_user_profile(user_input)
        
        # 2. Kaynak Araştırması (Content Curator Agent)
        resources = self.content_curator_agent.find_resources(profile)
        
        # 3. İlk Plan Oluşturma (Roadmap Agent)
        # Not: Tam müfredat oluşturmak pahalıdır, burada sadece ilk gün planını çekiyoruz
        # Gerçek uygulamada generate_curriculum çağrılır ve kaydedilir
        goal = profile.get("goal", "")
        level = profile.get("level", "beginner")
        
        # Demo için hızlı plan (gün 1)
        plan = self.roadmap_agent.get_day_plan(
            day=1,
            goal=goal,
            level=level
        )
        
        # Plan içine kaynakları ekle
        if plan and resources:
            plan["resources"] = resources[:3]
        
        return {
            "profile": profile, 
            "plan": plan, 
            "resources": resources
        }

    def run_daily_cycle(self, user_id: str, day_report: dict):
        """Günlük döngüyü çalıştırır: Değerlendirme -> Sonraki Plan."""
        
        # 1. Değerlendirme (Progress Agent)
        eval_metrics = self.progress_agent.evaluate(day_report)
        
        # 2. Profil güncelle (Memory'den)
        if self.memory:
            profile = self.memory.get_user_profile() or {}
        else:
            profile = {} # Fallback
            
        goal = profile.get("goal", "")
        level = profile.get("level", "beginner")
        
        # 3. Sonraki günün planı (Roadmap Agent)
        next_day = day_report.get("day", 1) + 1
        next_plan = self.roadmap_agent.get_day_plan(next_day, goal, level)
        
        # 4. Kaynak önerileri (Content Curator Agent - Opsiyonel, taze kaynaklar için)
        if next_plan:
            resources = self.content_curator_agent.find_resources(profile)
            next_plan["resources"] = resources[:2]
            
        return {
            "evaluation": eval_metrics, 
            "next_plan": next_plan
        }
