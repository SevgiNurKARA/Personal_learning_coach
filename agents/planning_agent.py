from typing import Dict, List, Optional

try:
    from tools.ai_service import AIService, get_ai_service
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False


class PlanningAgent:    
    def __init__(self, memory_service=None, ai_service: Optional['AIService'] = None):
        self.memory = memory_service
        self.ai_service = ai_service
        
        # AI servisi verilmediyse ve mümkünse otomatik al
        if self.ai_service is None and AI_AVAILABLE:
            try:
                self.ai_service = get_ai_service()
            except Exception:
                self.ai_service = None

    def generate_daily_plan(
        self, 
        profile: Dict, 
        resources: List[Dict], 
        day: int = 1,
        previous_evaluation: Optional[Dict] = None
    ) -> Dict:
        # AI servisi varsa akıllı plan oluştur
        if self.ai_service and self.ai_service._is_configured():
            plan = self.ai_service.generate_personalized_plan(profile, resources, day)
        else:
            plan = self._generate_basic_plan(profile, resources, day)
        
        # Önceki değerlendirmeye göre ayarlama yap
        if previous_evaluation:
            plan = self._adjust_plan_based_on_evaluation(plan, previous_evaluation)
        
        # Belleğe kaydet
        if self.memory:
            self.memory.append_daily_plan(plan)
        
        return plan

    def _generate_basic_plan(self, profile: Dict, resources: List[Dict], day: int) -> Dict:
        daily_time = profile.get("daily_time", 0.5)
        level = profile.get("level", "beginner")
        domain = profile.get("domain", "general")
        
        # Seviyeye göre görev dağılımı
        if level in ["beginner", "başlangıç"]:
            theory_ratio = 0.4
            practice_ratio = 0.4
            quiz_ratio = 0.2
        elif level in ["intermediate", "orta"]:
            theory_ratio = 0.3
            practice_ratio = 0.5
            quiz_ratio = 0.2
        else:
            theory_ratio = 0.2
            practice_ratio = 0.6
            quiz_ratio = 0.2
        
        total_minutes = int(daily_time * 60)
        
        # Günlük temalar (döngüsel)
        themes = [
            "Temel Kavramlar",
            "Veri Yapıları",
            "Kontrol Akışı",
            "Fonksiyonlar",
            "Modüller ve Paketler",
            "Hata Yönetimi",
            "Dosya İşlemleri"
        ]
        theme = themes[(day - 1) % len(themes)]
        
        plan = {
            "type": "learning_plan",
            "day": day,
            "theme": f"Gün {day} - {theme}",
            "total_duration_min": total_minutes,
            "tasks": [
                {
                    "task_id": 1,
                    "task": "Teori okuma",
                    "duration_min": int(total_minutes * theory_ratio),
                    "type": "theory",
                    "description": f"{theme} konusunu oku ve not al",
                    "priority": "high",
                    "completed": False
                },
                {
                    "task_id": 2,
                    "task": "Mini quiz",
                    "duration_min": int(total_minutes * quiz_ratio),
                    "type": "quiz",
                    "description": "Öğrenilenleri kısa bir quizle test et",
                    "priority": "medium",
                    "completed": False
                },
                {
                    "task_id": 3,
                    "task": "Pratik egzersiz",
                    "duration_min": int(total_minutes * practice_ratio),
                    "type": "practice",
                    "description": f"{theme} ile ilgili küçük bir uygulama yap",
                    "priority": "high",
                    "completed": False
                }
            ],
            "resources": resources[:3] if resources else [],
            "learning_objectives": [
                f"{theme} temel kavramlarını anlama",
                "Pratik uygulama yapabilme",
                "Quiz sorularını çözebilme"
            ],
            "tips": self._get_daily_tip(day),
            "domain": domain,
            "level": level
        }
        
        return plan

    def _adjust_plan_based_on_evaluation(self, plan: Dict, evaluation: Dict) -> Dict:
        daily_score = evaluation.get("daily_score", 0)
        performance_level = evaluation.get("performance_level", "average")
        
        # Düşük performansta daha fazla teori ve tekrar
        if performance_level == "needs_improvement" or daily_score < 20:
            plan["tips"] = "⚠️ Önceki gün zorlandınız. Bugün daha yavaş ilerleyin ve tekrar yapın."
            
            # Teori süresini artır
            for task in plan.get("tasks", []):
                if task.get("type") == "theory":
                    task["duration_min"] = int(task["duration_min"] * 1.3)
                    task["description"] += " (Ekstra tekrar önerilir)"
        
        # Yüksek performansta daha fazla pratik
        elif performance_level == "excellent" or daily_score >= 40:
            plan["tips"] = "🌟 Harika gidiyorsunuz! Bugün biraz daha zorlu konulara geçebilirsiniz."
            
            # Pratik süresini artır
            for task in plan.get("tasks", []):
                if task.get("type") == "practice":
                    task["duration_min"] = int(task["duration_min"] * 1.2)
                    task["description"] += " (İleri seviye egzersiz deneyin)"
        
        # Quiz analizi varsa zayıf konuları ekle
        quiz_analysis = evaluation.get("quiz_analysis", {})
        weak_topics = quiz_analysis.get("weak_topics", [])
        
        if weak_topics:
            plan["focus_areas"] = weak_topics
            plan["tips"] += f"\n📚 Şu konulara ekstra odaklanın: {', '.join(weak_topics)}"
        
        return plan

    def _get_daily_tip(self, day: int) -> str:
        """Gün numarasına göre ipucu döndürür."""
        tips = [
            "💡 Düzenli molalar verin, her 25 dakikada 5 dakika dinlenin.",
            "📝 Not almak öğrenmeyi pekiştirir, önemli noktaları yazın.",
            "🔄 Önceki günlerin notlarını gözden geçirin.",
            "💻 Kod yazarken hata yapmaktan korkmayın, hatalar öğretir.",
            "🎯 Küçük hedefler koyun ve başardığınızda kendinizi ödüllendirin.",
            "🤔 Anlamadığınız konuları araştırın ve sorular sorun.",
            "🏃 Pratik yapmak teoriden daha önemlidir, kod yazın!"
        ]
        return tips[(day - 1) % len(tips)]

    def get_weekly_overview(self, profile: Dict) -> Dict:
        daily_time = profile.get("daily_time", 1)
        domain = profile.get("domain", "general")
        
        weekly_themes = [
            "Temeller ve Kurulum",
            "Veri Tipleri ve Değişkenler",
            "Kontrol Yapıları",
            "Fonksiyonlar",
            "Veri Yapıları",
            "Dosya ve Hata Yönetimi",
            "Proje ve Tekrar"
        ]
        
        return {
            "type": "weekly_overview",
            "domain": domain,
            "total_hours": daily_time * 7,
            "days": [
                {"day": i + 1, "theme": theme, "duration_hours": daily_time}
                for i, theme in enumerate(weekly_themes)
            ],
            "goals": [
                f"{domain} temellerini öğrenmek",
                "Pratik projeler yapmak",
                "Quiz'lerde %70+ başarı sağlamak"
            ]
        }
