import json
import random
import time
import os


class Orchestrator:
    def __init__(self, audio_engine):
        self.audio_engine = audio_engine
        self.scenes = {}
        self.current_scene = None
        self.active_scene_data = None
        self.bed_channel = None
        self.last_update_time = time.time()
    
    def _validate_scenes(self, scenes_data):
        """Checks if all file paths in the scene data exist."""
        is_valid = True
        for scene_name, data in scenes_data.items():
            bed_info = data.get("bed", {})
            if "file" in bed_info and not os.path.exists(bed_info["file"]):
                print(f"Validation Error: Bed file not found for scene '{scene_name}': {bed_info['file']}")
                is_valid = False
            
            for oneshot in data.get("oneshots", []):
                if "file" in oneshot and not os.path.exists(oneshot["file"]):
                    print(f"Validation Error: Oneshot file not found for scene '{scene_name}': {oneshot['file']}")
                    is_valid = False
        return is_valid

    def load_scenes_from_file(self, filepath):
        try:
            with open(filepath, 'r') as f:
                scenes_data = json.load(f)
            if not self._validate_scenes(scenes_data):
                return False
            self.scenes = scenes_data
            print(f"Loaded {len(self.scenes)} scenes from {filepath}")
            return True
        except FileNotFoundError:
            print(f"Error: Scenes file not found: {filepath}")
            return False
        except json.JSONDecodeError as e:
            print(f"Error parsing scenes file: {e}")
            return False
    
    def play_scene(self, scene_name):
        if scene_name not in self.scenes:
            print(f"Error: Scene '{scene_name}' not found")
            return False
        
        # Stop current scene
        self.audio_engine.stop_all_sounds()
        
        # Load new scene
        self.current_scene = scene_name
        self.active_scene_data = self.scenes[scene_name]
        
        # Play bed sound
        bed_info = self.active_scene_data.get("bed")
        if bed_info and "file" in bed_info:
            bed_file = bed_info["file"]
            bed_volume = bed_info.get("volume", 0.7)
            self.bed_channel = self.audio_engine.play_sound(bed_file, loop=True, volume=bed_volume)
            print(f"Started scene: {scene_name}")
            return True
        else:
            print(f"Warning: Bed sound not configured for scene: {scene_name}")
            return False
    
    def update(self):
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
                # Play the one-shot
                filepath = oneshot.get("file")
                if filepath: # Path already validated at load time
                    volume_min = oneshot.get("volume_min", 0.5)
                    volume_max = oneshot.get("volume_max", 1.0)
                    volume = random.uniform(volume_min, volume_max)
                    
                    self.audio_engine.play_sound(filepath, loop=False, volume=volume)
    
    def get_available_scenes(self):
        return list(self.scenes.keys())
    
    def get_scene_keywords(self):
        """Returns a dictionary of scenes and their associated keywords."""
        return {
            scene: data.get("keywords", []) for scene, data in self.scenes.items()
        }

    def stop_current_scene(self):
        self.audio_engine.stop_all_sounds()
        self.current_scene = None
        self.active_scene_data = None
        self.bed_channel = None