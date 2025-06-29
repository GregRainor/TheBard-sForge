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
    
    def load_scenes_from_file(self, filepath):
        try:
            with open(filepath, 'r') as f:
                self.scenes = json.load(f)
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
        bed_file = self.active_scene_data.get("bed")
        if bed_file and os.path.exists(bed_file):
            self.bed_channel = self.audio_engine.play_sound(bed_file, loop=True, volume=0.7)
            print(f"Started scene: {scene_name}")
            return True
        else:
            print(f"Warning: Bed sound file not found: {bed_file}")
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
                if filepath and os.path.exists(filepath):
                    volume_min = oneshot.get("volume_min", 0.5)
                    volume_max = oneshot.get("volume_max", 1.0)
                    volume = random.uniform(volume_min, volume_max)
                    
                    self.audio_engine.play_sound(filepath, loop=False, volume=volume)
    
    def get_available_scenes(self):
        return list(self.scenes.keys())
    
    def stop_current_scene(self):
        self.audio_engine.stop_all_sounds()
        self.current_scene = None
        self.active_scene_data = None
        self.bed_channel = None