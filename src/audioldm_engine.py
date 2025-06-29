import torch
import scipy
import numpy as np
from diffusers import AudioLDMPipeline
import os
import tempfile
import time


class AudioLDMEngine:
    """AI Audio Generation Engine using AudioLDM pre-trained models."""
    
    def __init__(self):
        print("🔧 Initializing AudioLDM Engine...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"🎯 Using device: {self.device}")
        
        # Load AudioLDM model
        repo_id = "cvssp/audioldm-s-full-v2"
        print(f"📥 Loading AudioLDM model: {repo_id}")
        
        self.pipe = AudioLDMPipeline.from_pretrained(
            repo_id, 
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
        )
        self.pipe = self.pipe.to(self.device)
        
        # Create output directory
        self.output_dir = "generated_audio"
        os.makedirs(self.output_dir, exist_ok=True)
        
        print("✅ AudioLDM Engine initialized successfully!")
    
    def generate_audio(self, prompt, duration=10.0, steps=20):
        """Generate audio from text prompt using AudioLDM."""
        print(f"🎵 Generating audio: '{prompt}' ({duration}s)")
        
        start_time = time.time()
        
        # Generate audio
        audio = self.pipe(
            prompt, 
            num_inference_steps=steps, 
            audio_length_in_s=duration
        ).audios[0]
        
        generation_time = time.time() - start_time
        
        # Create filename with timestamp to avoid conflicts
        timestamp = int(time.time() * 1000)
        filename = f"generated_{timestamp}.wav"
        filepath = os.path.join(self.output_dir, filename)
        
        # Ensure audio is in correct format and normalize
        audio_normalized = audio / (np.max(np.abs(audio)) + 1e-8)  # Avoid division by zero
        
        # Convert to 16-bit PCM and save
        audio_16bit = (audio_normalized * 32767).astype(np.int16)
        scipy.io.wavfile.write(filepath, rate=16000, data=audio_16bit)
        
        print(f"⚡ Generated in {generation_time:.2f}s")
        print(f"💾 Saved to: {filepath}")
        
        return filepath, generation_time
    
    def generate_scene_audio(self, scene_description):
        """Generate multiple audio layers for a complete scene."""
        print(f"🎭 Generating scene: {scene_description}")
        
        # Define scene-specific prompts
        scene_prompts = {
            "tavern": [
                "medieval tavern ambiance with crackling fireplace",
                "distant medieval lute music",
                "muffled conversation and laughter in tavern",
                "clinking of medieval tankards and dishes"
            ],
            "forest": [
                "peaceful forest ambiance with birds chirping",
                "gentle wind through trees",
                "distant flowing stream",
                "rustling leaves and branches"
            ],
            "dungeon": [
                "dark dungeon ambiance with water dripping",
                "distant echoing footsteps",
                "ominous cave atmosphere",
                "metal chains rattling"
            ],
            "battle": [
                "epic medieval battle sounds",
                "sword clashing and armor clanking",
                "war cries and battle shouts",
                "dramatic orchestral battle music"
            ]
        }
        
        # Get prompts for scene or use description directly
        prompts = scene_prompts.get(scene_description.lower(), [scene_description])
        
        generated_files = []
        total_time = 0
        
        for i, prompt in enumerate(prompts):
            try:
                file_path, gen_time = self.generate_audio(prompt, duration=8.0)
                generated_files.append(file_path)
                total_time += gen_time
            except Exception as e:
                print(f"❌ Error generating audio for '{prompt}': {e}")
        
        print(f"🎉 Scene generation complete! {len(generated_files)} files in {total_time:.2f}s")
        return generated_files
    
    def get_gpu_memory_usage(self):
        """Get current GPU memory usage."""
        if torch.cuda.is_available():
            return torch.cuda.memory_allocated() / 1024**2  # MB
        return 0