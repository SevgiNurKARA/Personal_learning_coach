"""
Kullanıcı modeli ve yönetimi
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class User:
    """Kullanıcı veri yapısı."""
    user_id: str
    username: str
    email: str
    password_hash: str
    created_at: str
    selected_program: Optional[str] = None
    current_week: int = 1
    current_day: int = 1
    total_study_hours: float = 0.0
    completed_lessons: List[str] = None
    quiz_scores: List[Dict] = None
    daily_time_preference: float = 1.0
    learning_style: str = "karma"
    # Müfredat ve seviye bilgileri (DEPRECATED - geriye dönük uyumluluk için)
    curriculum: Optional[Dict] = None
    user_level: Optional[Dict] = None
    goal_input: Optional[Dict] = None
    completed_days: List[int] = None
    # Çoklu müfredat sistemi
    curriculums: List[Dict] = None  # Tüm müfredatlar
    active_curriculum_id: Optional[str] = None  # Aktif müfredat
    
    def __post_init__(self):
        if self.completed_lessons is None:
            self.completed_lessons = []
        if self.quiz_scores is None:
            self.quiz_scores = []
        if self.completed_days is None:
            self.completed_days = []
        if self.curriculums is None:
            self.curriculums = []
        
        # Eski tek müfredat varsa çoklu sisteme taşı
        if self.curriculum and not self.curriculums:
            curriculum_id = f"curr_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            self.curriculums = [{
                "id": curriculum_id,
                "curriculum": self.curriculum,
                "goal_input": self.goal_input,
                "user_level": self.user_level,
                "current_day": self.current_day,
                "completed_days": self.completed_days or [],
                "day_quiz_completed": {},
                "created_at": datetime.now().isoformat(),
                "status": "active"
            }]
            self.active_curriculum_id = curriculum_id


class UserManager:
    """Kullanıcı yönetimi sınıfı."""
    
    def __init__(self, data_path: str = "data/users.json"):
        self.data_path = Path(data_path)
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not self.data_path.exists():
            self._save_data({"users": {}})
    
    def _load_data(self) -> Dict:
        """Kullanıcı verilerini yükler."""
        with open(self.data_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def _save_data(self, data: Dict):
        """Kullanıcı verilerini kaydeder."""
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _hash_password(self, password: str) -> str:
        """Şifreyi hashler."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register(self, username: str, email: str, password: str) -> tuple[bool, str]:
        """
        Yeni kullanıcı kaydı.
        
        Returns:
            (başarılı_mı, mesaj)
        """
        data = self._load_data()
        
        # Email kontrolü
        for user_data in data["users"].values():
            if user_data["email"] == email:
                return False, "Bu email zaten kayıtlı!"
            if user_data["username"] == username:
                return False, "Bu kullanıcı adı zaten alınmış!"
        
        # Yeni kullanıcı oluştur
        user_id = f"user_{len(data['users']) + 1}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        user = User(
            user_id=user_id,
            username=username,
            email=email,
            password_hash=self._hash_password(password),
            created_at=datetime.now().isoformat()
        )
        
        data["users"][user_id] = asdict(user)
        self._save_data(data)
        
        return True, user_id
    
    def login(self, email: str, password: str) -> tuple[bool, Optional[User]]:
        """
        Kullanıcı girişi.
        
        Returns:
            (başarılı_mı, kullanıcı)
        """
        data = self._load_data()
        password_hash = self._hash_password(password)
        
        for user_id, user_data in data["users"].items():
            if user_data["email"] == email and user_data["password_hash"] == password_hash:
                return True, User(**user_data)
        
        return False, None
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Kullanıcı bilgilerini getirir."""
        data = self._load_data()
        if user_id in data["users"]:
            return User(**data["users"][user_id])
        return None
    
    def update_user(self, user: User):
        """Kullanıcı bilgilerini günceller."""
        data = self._load_data()
        data["users"][user.user_id] = asdict(user)
        self._save_data(data)
    
    def select_program(self, user_id: str, program_id: str):
        """Kullanıcıya program atar."""
        user = self.get_user(user_id)
        if user:
            user.selected_program = program_id
            user.current_week = 1
            user.current_day = 1
            self.update_user(user)
    
    def record_progress(self, user_id: str, lesson_id: str, study_hours: float, quiz_score: Optional[int] = None):
        """İlerleme kaydeder."""
        user = self.get_user(user_id)
        if user:
            if lesson_id not in user.completed_lessons:
                user.completed_lessons.append(lesson_id)
            user.total_study_hours += study_hours
            
            if quiz_score is not None:
                user.quiz_scores.append({
                    "lesson_id": lesson_id,
                    "score": quiz_score,
                    "date": datetime.now().isoformat()
                })
            
            self.update_user(user)
    
    def advance_day(self, user_id: str):
        """Sonraki güne geçer."""
        user = self.get_user(user_id)
        if user:
            user.current_day += 1
            if user.current_day > 7:
                user.current_day = 1
                user.current_week += 1
            self.update_user(user)
    
    def get_user_stats(self, user_id: str) -> Dict:
        """Kullanıcı istatistiklerini döndürür."""
        user = self.get_user(user_id)
        if not user:
            return {}
        
        avg_quiz = 0
        if user.quiz_scores:
            avg_quiz = sum(q["score"] for q in user.quiz_scores) / len(user.quiz_scores)
        
        return {
            "total_lessons": len(user.completed_lessons),
            "total_hours": round(user.total_study_hours, 1),
            "average_quiz_score": round(avg_quiz, 1),
            "current_week": user.current_week,
            "current_day": user.current_day,
            "quiz_count": len(user.quiz_scores)
        }
    
    def save_curriculum(self, user_id: str, curriculum: Dict, goal_input: Dict, user_level: Dict, current_day: int = 1, completed_days: List[int] = None, curriculum_id: str = None):
        """Kullanıcının müfredatını ve ilerlemesini kaydeder - çoklu müfredat destekli."""
        user = self.get_user(user_id)
        if user:
            # Yeni müfredat ID'si oluştur
            if not curriculum_id:
                curriculum_id = f"curr_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Yeni müfredat objesi
            new_curriculum = {
                "id": curriculum_id,
                "curriculum": curriculum,
                "goal_input": goal_input,
                "user_level": user_level,
                "current_day": current_day,
                "completed_days": completed_days or [],
                "day_quiz_completed": {},
                "created_at": datetime.now().isoformat(),
                "status": "active"
            }
            
            # Mevcut müfredatları kontrol et
            if not user.curriculums:
                user.curriculums = []
            
            # Aynı ID varsa güncelle, yoksa ekle
            found = False
            for i, curr in enumerate(user.curriculums):
                if curr.get("id") == curriculum_id:
                    user.curriculums[i] = new_curriculum
                    found = True
                    break
            
            if not found:
                user.curriculums.append(new_curriculum)
            
            # Aktif müfredat olarak ayarla
            user.active_curriculum_id = curriculum_id
            
            # Geriye dönük uyumluluk için eski alanları da güncelle
            user.curriculum = curriculum
            user.goal_input = goal_input
            user.user_level = user_level
            user.current_day = current_day
            user.completed_days = completed_days or []
            user.selected_program = goal_input.get("goal", "")[:50]
            
            self.update_user(user)
            return curriculum_id
    
    def load_curriculum(self, user_id: str, curriculum_id: str = None) -> Optional[Dict]:
        """Kullanıcının müfredatını yükler - çoklu müfredat destekli."""
        user = self.get_user(user_id)
        if not user:
            return None
        
        # Belirli bir müfredat istendi mi?
        if curriculum_id:
            for curr in user.curriculums or []:
                if curr.get("id") == curriculum_id:
                    return curr
            return None
        
        # Aktif müfredatı yükle
        if user.active_curriculum_id:
            for curr in user.curriculums or []:
                if curr.get("id") == user.active_curriculum_id:
                    return curr
        
        # Geriye dönük uyumluluk - eski tek müfredat
        if user.curriculum:
            return {
                "curriculum": user.curriculum,
                "goal_input": user.goal_input,
                "user_level": user.user_level,
                "current_day": user.current_day,
                "completed_days": user.completed_days or [],
                "day_quiz_completed": {}
            }
        
        return None
    
    def get_all_curriculums(self, user_id: str) -> List[Dict]:
        """Kullanıcının tüm müfredatlarını getirir."""
        user = self.get_user(user_id)
        if user and user.curriculums:
            return user.curriculums
        return []
    
    def set_active_curriculum(self, user_id: str, curriculum_id: str):
        """Aktif müfredatı değiştirir."""
        user = self.get_user(user_id)
        if user:
            # Müfredat var mı kontrol et
            for curr in user.curriculums or []:
                if curr.get("id") == curriculum_id:
                    user.active_curriculum_id = curriculum_id
                    
                    # Eski alanları da güncelle
                    user.curriculum = curr.get("curriculum")
                    user.goal_input = curr.get("goal_input")
                    user.user_level = curr.get("user_level")
                    user.current_day = curr.get("current_day", 1)
                    user.completed_days = curr.get("completed_days", [])
                    
                    self.update_user(user)
                    return True
            return False
        return False
    
    def archive_curriculum(self, user_id: str, curriculum_id: str):
        """Müfredatı arşivler (siler değil)."""
        user = self.get_user(user_id)
        if user and user.curriculums:
            for curr in user.curriculums:
                if curr.get("id") == curriculum_id:
                    curr["status"] = "archived"
                    curr["archived_at"] = datetime.now().isoformat()
                    self.update_user(user)
                    return True
        return False
    
    def update_progress(self, user_id: str, current_day: int, completed_days: List[int], day_quiz_completed: Dict = None):
        """Kullanıcının güncel ilerlemesini günceller - aktif müfredat için."""
        user = self.get_user(user_id)
        if user:
            # Aktif müfredatı bul ve güncelle
            if user.active_curriculum_id and user.curriculums:
                for curr in user.curriculums:
                    if curr.get("id") == user.active_curriculum_id:
                        curr["current_day"] = current_day
                        curr["completed_days"] = completed_days
                        if day_quiz_completed is not None:
                            curr["day_quiz_completed"] = day_quiz_completed
                        break
            
            # Eski alanları da güncelle
            user.current_day = current_day
            user.completed_days = completed_days
            self.update_user(user)

