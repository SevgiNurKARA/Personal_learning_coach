from typing import Dict, List, Optional
from tools.quiz_scoring import QuizScorer, QuizQuestion, QuizResult


class ProgressAgent:
    
    def __init__(self, memory_service=None):
        self.memory = memory_service
        self.quiz_scorer = QuizScorer()

# ... (methods from evaluation_agent.py) ...


    def evaluate(self, day_report: Dict) -> Dict:
        score = 0
        completed = day_report.get("completed_tasks", 0)
        quiz = day_report.get("quiz_score", None)
        diff = day_report.get("perceived_difficulty", 3)

        # Temel puan hesaplama
        score = completed * 10
        
        if quiz is not None:
            score += int(quiz / 10)
            # Zorluk seviyesine göre ayarlama
            score = max(0, score - (diff - 3) * 5)

        # Performans seviyesi belirleme
        performance_level = self._determine_performance_level(score, quiz, diff)
        
        # Öneriler oluştur
        suggestions = self._generate_suggestions(score, quiz, diff, completed)

        metrics = {
            "daily_score": score,
            "performance_level": performance_level,
            "suggestions": suggestions,
            "raw": day_report
        }
        
        if self.memory:
            self.memory.append_performance(metrics)
        
        return metrics

    def evaluate_with_quiz(
        self, 
        day_report: Dict, 
        quiz_answers: Dict[str, str],
        quiz_questions: List[QuizQuestion]
    ) -> Dict:
        # Quiz analizi
        quiz_result = self.quiz_scorer.analyze_quiz(quiz_answers, quiz_questions)
        
        # Temel değerlendirme
        base_metrics = self.evaluate(day_report)
        
        # Quiz sonuçlarını ekle
        base_metrics["quiz_analysis"] = {
            "score_percentage": quiz_result.score_percentage,
            "correct_count": quiz_result.correct_count,
            "total_questions": quiz_result.total_questions,
            "topic_scores": quiz_result.topic_scores,
            "weak_topics": quiz_result.weak_topics,
            "strong_topics": quiz_result.strong_topics
        }
        
        # Quiz bazlı öneriler ekle
        quiz_suggestions = self.quiz_scorer.get_improvement_suggestions(quiz_result)
        base_metrics["suggestions"].extend(quiz_suggestions)
        
        return base_metrics

    def _determine_performance_level(self, score: int, quiz: Optional[int], diff: int) -> str:
        if score >= 40 and (quiz is None or quiz >= 80):
            return "excellent"
        elif score >= 30 and (quiz is None or quiz >= 60):
            return "good"
        elif score >= 20:
            return "average"
        else:
            return "needs_improvement"

    def _generate_suggestions(
        self, 
        score: int, 
        quiz: Optional[int], 
        diff: int, 
        completed: int
    ) -> List[str]:
        """Performansa göre öneriler oluşturur."""
        suggestions = []
        
        # Tamamlanan görev sayısına göre
        if completed < 2:
            suggestions.append("📋 Daha fazla görev tamamlamaya çalışın.")
        elif completed >= 3:
            suggestions.append("✅ Görevleri tamamlamada başarılısınız!")
        
        # Quiz puanına göre
        if quiz is not None:
            if quiz < 50:
                suggestions.append("📚 Konuları tekrar gözden geçirmenizi öneririz.")
            elif quiz < 70:
                suggestions.append("📖 İyi gidiyorsunuz, biraz daha pratik yapın.")
            else:
                suggestions.append("🌟 Quiz performansınız harika!")
        
        # Zorluk algısına göre
        if diff >= 4:
            suggestions.append("💡 Zorluk yüksek görünüyor, daha basit konularla başlayabilirsiniz.")
        elif diff <= 2:
            suggestions.append("🚀 Hazırsanız daha ileri konulara geçebilirsiniz.")
        
        return suggestions

    def generate_quiz_for_topic(self, topic: str, num_questions: int = 5) -> List[QuizQuestion]:
        return self.quiz_scorer.generate_sample_quiz(topic, num_questions)

    def get_progress_summary(self) -> Dict:
        if not self.memory:
            return {"message": "Bellek servisi yapılandırılmamış"}
        
        # Performans geçmişini al (eğer memory'de varsa)
        try:
            data = self.memory._read()
            performance_history = data.get("performance", [])
            
            if not performance_history:
                return {"message": "Henüz performans verisi yok"}
            
            total_scores = [p.get("daily_score", 0) for p in performance_history]
            avg_score = sum(total_scores) / len(total_scores) if total_scores else 0
            
            return {
                "total_days": len(performance_history),
                "average_score": round(avg_score, 2),
                "best_score": max(total_scores) if total_scores else 0,
                "trend": "improving" if len(total_scores) > 1 and total_scores[-1] > total_scores[0] else "stable"
            }
        except Exception:
            return {"message": "İlerleme verisi alınamadı"}

# Singleton
_progress_agent = None

def get_progress_agent() -> ProgressAgent:
    global _progress_agent
    if _progress_agent is None:
        _progress_agent = ProgressAgent()
    return _progress_agent
