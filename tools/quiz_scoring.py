from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class QuizQuestion:
    """Quiz sorusu veri yapısı."""
    question_id: str
    question: str
    options: List[str]
    correct_answer: str
    topic: str = ""
    difficulty: int = 1  # 1-5 arası


@dataclass
class QuizResult:
    """Quiz sonuç veri yapısı."""
    total_questions: int
    correct_count: int
    wrong_count: int
    score_percentage: int
    topic_scores: Dict[str, int]
    weak_topics: List[str]
    strong_topics: List[str]


class QuizScorer:
    """Quiz puanlama ve analiz sınıfı."""
    
    def __init__(self):
        self.quiz_history: List[QuizResult] = []
    
    def score_quiz(self, answers: Dict[str, str], key_answers: Dict[str, str]) -> int:
        """
        Quiz cevaplarını puanlar ve yüzde olarak doğru cevap oranını döndürür.
        
        Args:
            answers: Kullanıcının verdiği cevaplar {soru_id: cevap}
            key_answers: Doğru cevaplar {soru_id: doğru_cevap}
        
        Returns:
            Yüzde olarak puan (0-100)
        """
        total = len(key_answers)
        if total == 0:
            return 0
        
        correct = sum(1 for k, v in key_answers.items() if answers.get(k) == v)
        return int((correct / total) * 100)
    
    def analyze_quiz(
        self, 
        answers: Dict[str, str], 
        questions: List[QuizQuestion]
    ) -> QuizResult:
        """
        Quiz sonuçlarını detaylı analiz eder.
        
        Args:
            answers: Kullanıcının verdiği cevaplar
            questions: Quiz soruları listesi
        
        Returns:
            QuizResult objesi
        """
        total = len(questions)
        correct_count = 0
        topic_correct: Dict[str, int] = {}
        topic_total: Dict[str, int] = {}
        
        for q in questions:
            topic = q.topic or "general"
            topic_total[topic] = topic_total.get(topic, 0) + 1
            
            if answers.get(q.question_id) == q.correct_answer:
                correct_count += 1
                topic_correct[topic] = topic_correct.get(topic, 0) + 1
        
        # Konu bazlı puanları hesapla
        topic_scores = {}
        weak_topics = []
        strong_topics = []
        
        for topic, total_q in topic_total.items():
            correct_q = topic_correct.get(topic, 0)
            score = int((correct_q / total_q) * 100) if total_q > 0 else 0
            topic_scores[topic] = score
            
            if score < 60:
                weak_topics.append(topic)
            elif score >= 80:
                strong_topics.append(topic)
        
        result = QuizResult(
            total_questions=total,
            correct_count=correct_count,
            wrong_count=total - correct_count,
            score_percentage=int((correct_count / total) * 100) if total > 0 else 0,
            topic_scores=topic_scores,
            weak_topics=weak_topics,
            strong_topics=strong_topics
        )
        
        self.quiz_history.append(result)
        return result
    
    def generate_sample_quiz(self, topic: str, num_questions: int = 5) -> List[QuizQuestion]:
        """
        Belirli bir konu için örnek quiz soruları üretir.
        
        Args:
            topic: Konu adı
            num_questions: Soru sayısı
        
        Returns:
            QuizQuestion listesi
        """
        # Python konusu için örnek sorular
        python_questions = [
            QuizQuestion(
                question_id="py_1",
                question="Python'da liste oluşturmak için hangi parantez kullanılır?",
                options=["()", "[]", "{}", "<>"],
                correct_answer="[]",
                topic="python_basics",
                difficulty=1
            ),
            QuizQuestion(
                question_id="py_2",
                question="Python'da yorum satırı nasıl başlar?",
                options=["//", "#", "/*", "--"],
                correct_answer="#",
                topic="python_basics",
                difficulty=1
            ),
            QuizQuestion(
                question_id="py_3",
                question="'len()' fonksiyonu ne döndürür?",
                options=["Veri tipi", "Uzunluk", "Değer", "İndeks"],
                correct_answer="Uzunluk",
                topic="python_functions",
                difficulty=2
            ),
            QuizQuestion(
                question_id="py_4",
                question="Python'da dictionary oluşturmak için hangi parantez kullanılır?",
                options=["()", "[]", "{}", "<>"],
                correct_answer="{}",
                topic="python_data_structures",
                difficulty=2
            ),
            QuizQuestion(
                question_id="py_5",
                question="'for i in range(5):' döngüsü kaç kez çalışır?",
                options=["4", "5", "6", "Sonsuz"],
                correct_answer="5",
                topic="python_loops",
                difficulty=2
            ),
        ]
        
        if "python" in topic.lower():
            return python_questions[:num_questions]
        
        # Genel sorular
        return [
            QuizQuestion(
                question_id=f"gen_{i}",
                question=f"Örnek soru {i+1} - {topic}",
                options=["A", "B", "C", "D"],
                correct_answer="A",
                topic=topic,
                difficulty=1
            )
            for i in range(num_questions)
        ]
    
    def get_improvement_suggestions(self, result: QuizResult) -> List[str]:
        """
        Quiz sonucuna göre gelişim önerileri sunar.
        
        Args:
            result: QuizResult objesi
        
        Returns:
            Öneri listesi
        """
        suggestions = []
        
        if result.score_percentage < 50:
            suggestions.append("📚 Temel konuları tekrar gözden geçirmenizi öneririz.")
        elif result.score_percentage < 70:
            suggestions.append("📖 İyi gidiyorsunuz! Biraz daha pratik yaparak pekiştirebilirsiniz.")
        else:
            suggestions.append("🌟 Harika! Bu konuda güçlü bir temele sahipsiniz.")
        
        for topic in result.weak_topics:
            suggestions.append(f"⚠️ '{topic}' konusunda daha fazla çalışmanız gerekiyor.")
        
        for topic in result.strong_topics:
            suggestions.append(f"✅ '{topic}' konusunda başarılısınız!")
        
        return suggestions


# Geriye dönük uyumluluk için fonksiyon
def score_quiz(answers: Dict, key_answers: Dict) -> int:
    """Score the quiz and return the percentage of correct answers."""
    scorer = QuizScorer()
    return scorer.score_quiz(answers, key_answers)
