from transformers import pipeline
import torch
import re
from typing import Optional, Dict, List, Any


class NLPInterpreter:
    def __init__(self):
        # Force CPU for NLP to avoid RTX 5090 compatibility issues
        self.device = "cpu"
        print(f"🧠 NLP Interpreter using device: {self.device}")
        
        try:
            self.classifier = pipeline(
                "zero-shot-classification",
                model="facebook/bart-large-mnli",
                device=-1  # Force CPU for compatibility
            )
            print(f"✅ NLP model loaded successfully on {self.device.upper()}")
        except Exception as e:
            print(f"⚠️ Could not load NLP model: {e}")
            print("🔄 Using keyword-based classification fallback")
            self.classifier = None
    
    def _extract_keywords(self, text: str) -> List[str]:
        # Simple keyword extraction - convert to lowercase and split
        text = text.lower()
        # Remove punctuation and split into words
        words = re.findall(r'\b\w+\b', text)
        return words
    
    def _match_keywords_to_scene(self, keywords: List[str], scene_keywords: Dict[str, List[str]]) -> Optional[str]:
        scene_scores = {}
        
        for scene, scene_words in scene_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in scene_words:
                    score += 1
            scene_scores[scene] = score
        
        if scene_scores and max(scene_scores.values()) > 0:
            return max(scene_scores, key=scene_scores.get)
        
        return None
    
    def _classify_with_model(self, text: str, scene_labels: List[str]) -> Optional[str]:
        if not self.classifier:
            return None
        
        try:
            result = self.classifier(text, scene_labels)
            
            # Get the highest scoring label with confidence > 0.5
            if result['scores'][0] > 0.5:
                return result['labels'][0]
        except Exception as e:
            print(f"🧠 NLP classification error: {e}")
            print("🔄 Falling back to keyword matching only")
        
        return None
    
    def interpret_prompt(self, text: str, scene_data: Dict[str, Any]) -> Optional[str]:
        if not text or not text.strip():
            return None
        
        scene_keywords = {name: data.get("keywords", []) for name, data in scene_data.items()}
        scene_labels = list(scene_data.keys())

        # First try keyword matching (fast and reliable)
        keywords = self._extract_keywords(text)
        keyword_result = self._match_keywords_to_scene(keywords, scene_keywords)
        
        if keyword_result:
            return keyword_result
        
        # Fallback to model-based classification
        model_result = self._classify_with_model(text, scene_labels)
        
        return model_result