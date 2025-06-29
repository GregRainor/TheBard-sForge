import json
import random
import time
import os
from typing import Optional, Dict, Any, List
from audio_engine import AudioEngine
from audio_generator import AudioGenerator


class GenerativeOrchestrator:
    """
    Enhanced orchestrator that can use both pre-recorded and generated audio.
    V1.0 - The Generative Leap
    """
    
    def __init__(self, audio_engine: AudioEngine):
        self.audio_engine = audio_engine
        self.audio_generator = AudioGenerator()
        self.scenes = {}
        self.current_scene = None
        self.active_scene_data = None
        self.bed_channel = None
        self.last_update_time = time.time()
        self.generation_enabled = True
        
        print("🚀 Generative Orchestrator V1.0 initialized")
        print(f"📊 Cache info: {self.audio_generator.get_cache_info()}")
    
    def _validate_scenes(self, scenes_data: Dict) -> bool:
        """Validates scene data, allowing for generated audio fallbacks."""
        is_valid = True
        for scene_name, data in scenes_data.items():
            bed_info = data.get("bed", {})
            
            # If file exists, use it; otherwise we can generate
            if "file" in bed_info and bed_info["file"]:
                if not os.path.exists(bed_info["file"]):
                    print(f"Info: Bed file not found for scene '{scene_name}': {bed_info['file']} (will generate)")
            
            # Validate oneshots (can be generated if missing)
            for oneshot in data.get("oneshots", []):
                if "file" in oneshot and oneshot["file"]:
                    if not os.path.exists(oneshot["file"]):
                        print(f"Info: Oneshot file not found for scene '{scene_name}': {oneshot['file']} (will generate)")
        
        return is_valid
    
    def load_scenes_from_file(self, filepath: str) -> bool:
        """Load scenes from JSON file."""
        try:
            with open(filepath, 'r') as f:
                scenes_data = json.load(f)
            
            self._validate_scenes(scenes_data)
            self.scenes = scenes_data
            print(f"✅ Loaded {len(self.scenes)} scenes from {filepath}")
            return True
            
        except FileNotFoundError:
            print(f"❌ Error: Scenes file not found: {filepath}")
            return False
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing scenes file: {e}")
            return False
    
    def _get_audio_file(self, audio_config: Dict, context: str = "") -> Optional[str]:
        """
        Get audio file path, generating if needed.
        audio_config can have 'file' and/or 'prompt' fields.
        """
        # Try to use existing file first
        if "file" in audio_config and os.path.exists(audio_config["file"]):
            return audio_config["file"]
        
        # Generate audio if we have a prompt or can infer one
        if self.generation_enabled:
            prompt = audio_config.get("prompt", "")
            
            # If no prompt but we have a broken file path, try to infer from filename
            if not prompt and "file" in audio_config:
                filename = os.path.basename(audio_config["file"])
                prompt = filename.replace("_", " ").replace(".wav", "").replace(".mp3", "")
            
            # Add context to prompt
            if context and prompt:
                prompt = f"{context} {prompt}"
            elif context and not prompt:
                prompt = context
            
            if prompt:
                duration = audio_config.get("duration", 3.0)
                sound_type = audio_config.get("type", "ambient")
                
                print(f"🎵 Generating audio for: '{prompt}'")
                generated_file = self.audio_generator.generate_sound(prompt, duration, sound_type)
                
                if generated_file:
                    return generated_file
                else:
                    print(f"⚠️ Failed to generate audio for '{prompt}'")
        
        return None
    
    def play_scene(self, scene_name: str) -> bool:
        """Play a scene using both pre-recorded and generated audio."""
        if scene_name not in self.scenes:
            print(f"❌ Error: Scene '{scene_name}' not found")
            return False
        
        print(f"🎬 Starting scene: {scene_name}")
        
        # Stop current scene
        self.audio_engine.stop_all_sounds()
        
        # Load new scene
        self.current_scene = scene_name
        self.active_scene_data = self.scenes[scene_name]
        
        # Play bed sound (background ambiance)
        bed_info = self.active_scene_data.get("bed", {})
        if bed_info:
            bed_file = self._get_audio_file(bed_info, f"{scene_name} ambient background")
            
            if bed_file:
                bed_volume = bed_info.get("volume", 0.7)
                self.bed_channel = self.audio_engine.play_sound(bed_file, loop=True, volume=bed_volume)
                print(f"✅ Scene '{scene_name}' started with audio: {os.path.basename(bed_file)}")
                return True
            else:
                print(f"⚠️ Warning: Could not load or generate bed sound for scene: {scene_name}")
                return False
        else:
            print(f"⚠️ Warning: No bed sound configured for scene: {scene_name}")
            return False
    
    def update(self):
        """Update the orchestrator, handling both pre-recorded and generated oneshots."""
        if not self.current_scene or not self.active_scene_data:
            return
        
        current_time = time.time()
        delta_time = current_time - self.last_update_time
        self.last_update_time = current_time
        
        # Process one-shots
        oneshots = self.active_scene_data.get("oneshots", [])
        for oneshot in oneshots:
            prob_per_sec = oneshot.get("prob_per_sec", 0)
            
            # Calculate probability for this frame based on delta time
            frame_probability = prob_per_sec * delta_time
            
            if random.random() < frame_probability:
                # Get the oneshot audio file (generate if needed)
                oneshot_file = self._get_audio_file(oneshot, f"{self.current_scene} oneshot")
                
                if oneshot_file:
                    volume_min = oneshot.get("volume_min", 0.5)
                    volume_max = oneshot.get("volume_max", 1.0)
                    volume = random.uniform(volume_min, volume_max)
                    
                    self.audio_engine.play_sound(oneshot_file, loop=False, volume=volume)
                    print(f"🔊 Playing oneshot: {os.path.basename(oneshot_file)}")
    
    def generate_scene_on_demand(self, scene_description: str, duration: float = 30.0) -> bool:
        """
        Generate a complete scene on-demand from a text description.
        This is the ultimate V1.0 feature!
        """
        print(f"🎭 Generating scene on-demand: '{scene_description}'")
        
        # Stop current scene
        self.audio_engine.stop_all_sounds()
        
        # Generate background ambiance
        print("🎵 Generating background ambiance...")
        bed_file = self.audio_generator.generate_sound(
            f"ambient background {scene_description}", 
            duration=duration, 
            sound_type="ambient"
        )
        
        if bed_file:
            self.bed_channel = self.audio_engine.play_sound(bed_file, loop=True, volume=0.6)
            print(f"✅ Generated scene background: {os.path.basename(bed_file)}")
            
            # Set up dynamic generation context
            self.current_scene = f"generated_{int(time.time())}"
            self.active_scene_data = {
                "bed": {"file": bed_file, "volume": 0.6},
                "oneshots": []
            }
            
            return True
        else:
            print("❌ Failed to generate scene background")
            return False
    
    def add_dynamic_oneshot(self, sound_description: str, probability: float = 0.05):
        """Add a dynamically generated oneshot to the current scene."""
        if not self.active_scene_data:
            print("❌ No active scene to add oneshot to")
            return
        
        oneshot_config = {
            "prompt": sound_description,
            "prob_per_sec": probability,
            "volume_min": 0.4,
            "volume_max": 0.8,
            "duration": 2.0,
            "type": "oneshot"
        }
        
        self.active_scene_data["oneshots"].append(oneshot_config)
        print(f"➕ Added dynamic oneshot: '{sound_description}'")
    
    def set_generation_enabled(self, enabled: bool):
        """Enable or disable audio generation (fallback to pre-recorded only)."""
        self.generation_enabled = enabled
        status = "enabled" if enabled else "disabled"
        print(f"🔧 Audio generation {status}")
    
    def get_available_scenes(self) -> List[str]:
        """Get list of available scene names."""
        return list(self.scenes.keys())
    
    def get_scene_keywords(self) -> Dict[str, List[str]]:
        """Get scene keywords for NLP interpretation."""
        return {
            scene: data.get("keywords", []) for scene, data in self.scenes.items()
        }
    
    def stop_current_scene(self):
        """Stop the current scene."""
        self.audio_engine.stop_all_sounds()
        self.current_scene = None
        self.active_scene_data = None
        self.bed_channel = None
        print("🛑 Scene stopped")
    
    def get_generation_stats(self) -> Dict:
        """Get statistics about audio generation."""
        cache_info = self.audio_generator.get_cache_info()
        return {
            "cache_files": cache_info["files"],
            "cache_size_mb": cache_info["size_mb"],
            "generation_enabled": self.generation_enabled,
            "current_scene": self.current_scene
        }
    
    def clear_generated_cache(self):
        """Clear the generated audio cache."""
        self.audio_generator.clear_cache()
        print("🗑️ Generated audio cache cleared")