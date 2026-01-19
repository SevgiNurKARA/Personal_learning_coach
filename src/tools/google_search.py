from typing import List, Dict, Optional
import os

try:
    from googleapiclient.discovery import build
    GOOGLE_API_AVAILABLE = True
except ImportError:
    GOOGLE_API_AVAILABLE = False


class GoogleSearchTool:    
    def __init__(self, api_key: Optional[str] = None, search_engine_id: Optional[str] = None):
        self.api_key = api_key or os.getenv("GOOGLE_SEARCH_API_KEY", "")
        self.search_engine_id = search_engine_id or os.getenv("GOOGLE_SEARCH_ENGINE_ID", "")
        self.service = None
        
        # API yapılandırılmışsa servisi başlat
        if self._is_configured() and GOOGLE_API_AVAILABLE:
            try:
                self.service = build("customsearch", "v1", developerKey=self.api_key)
            except Exception as e:
                print(f"⚠️ Google Search API başlatılamadı: {e}")
                self.service = None
    
    def _is_configured(self) -> bool:
        return bool(self.api_key and self.search_engine_id)
    
    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        # API yapılandırılmamışsa mock veri döndür
        if not self._is_configured() or not self.service:
            return self._mock_search(query, max_results)
        
        try:
            # Gerçek API çağrısı
            result = self.service.cse().list(
                q=query,
                cx=self.search_engine_id,
                num=min(max_results, 10)  # Google API max 10 sonuç döndürür
            ).execute()
            
            items = result.get("items", [])
            
            return [
                {
                    "title": item.get("title", ""),
                    "url": item.get("link", ""),
                    "snippet": item.get("snippet", ""),
                    "source": "google_api"
                }
                for item in items
            ]
        
        except Exception as e:
            print(f"⚠️ Arama hatası: {e}")
            return self._mock_search(query, max_results)
    
    def search_learning_resources(
        self, 
        topic: str, 
        level: str = "beginner",
        language: str = "tr",
        max_results: int = 5
    ) -> List[Dict]:
        # Seviye çevirisi
        level_map = {
            "beginner": "başlangıç",
            "başlangıç": "başlangıç",
            "intermediate": "orta seviye",
            "orta": "orta seviye",
            "advanced": "ileri seviye",
            "ileri": "ileri seviye"
        }
        level_tr = level_map.get(level.lower(), level)
        
        # Optimize edilmiş sorgu oluştur
        query = f"{topic} {level_tr} eğitim tutorial öğren"
        
        results = self.search(query, max_results)
        
        # Sonuçları zenginleştir
        for result in results:
            result["topic"] = topic
            result["level"] = level
            result["resource_type"] = self._classify_resource(result.get("url", ""))
        
        return results
    
    def _classify_resource(self, url: str) -> str:
        url_lower = url.lower()
        
        if "youtube.com" in url_lower or "youtu.be" in url_lower:
            return "video"
        elif "github.com" in url_lower:
            return "code_repository"
        elif "medium.com" in url_lower or "dev.to" in url_lower:
            return "article"
        elif "docs." in url_lower or "documentation" in url_lower:
            return "documentation"
        elif "udemy.com" in url_lower or "coursera.org" in url_lower or "edx.org" in url_lower:
            return "course"
        else:
            return "website"
    
    def _mock_search(self, query: str, max_results: int) -> List[Dict]:
        # Konu bazlı örnek kaynaklar
        mock_resources = {
            "python": [
                {
                    "title": "Python Resmi Dokümantasyonu",
                    "url": "https://docs.python.org/3/tutorial/",
                    "snippet": "Python programlama diline resmi giriş rehberi.",
                    "resource_type": "documentation"
                },
                {
                    "title": "Python Başlangıç Kursu - YouTube",
                    "url": "https://www.youtube.com/watch?v=example",
                    "snippet": "Sıfırdan Python öğrenmek için kapsamlı video serisi.",
                    "resource_type": "video"
                },
                {
                    "title": "W3Schools Python Tutorial",
                    "url": "https://www.w3schools.com/python/",
                    "snippet": "İnteraktif Python öğrenme platformu.",
                    "resource_type": "website"
                },
                {
                    "title": "Real Python - Tutorials",
                    "url": "https://realpython.com/",
                    "snippet": "Python tutorials, guides, and resources.",
                    "resource_type": "article"
                },
                {
                    "title": "Python Egzersizleri",
                    "url": "https://www.hackerrank.com/domains/python",
                    "snippet": "Python pratik problemleri ve alıştırmaları.",
                    "resource_type": "website"
                }
            ],
            "default": [
                {
                    "title": f"Sonuç {i+1}: {query}",
                    "url": f"https://example.org/resource/{i+1}",
                    "snippet": f"{query} konusu hakkında örnek kaynak.",
                    "resource_type": "website"
                }
                for i in range(max_results)
            ]
        }
        
        # Python içeren sorgular için özel sonuçlar
        if "python" in query.lower():
            results = mock_resources["python"][:max_results]
        else:
            results = mock_resources["default"][:max_results]
        
        # Mock olduğunu belirt
        for result in results:
            result["source"] = "mock"
        
        return results


# Geriye dönük uyumluluk için basit fonksiyon
def google_search(query: str, max_results: int = 5) -> List[Dict]:
    """Basit arama fonksiyonu."""
    tool = GoogleSearchTool()
    return tool.search(query, max_results)
