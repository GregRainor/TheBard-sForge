#!/usr/bin/env python3

import torch
import numpy as np
import time
import os
import hashlib
import soundfile as sf
from typing import Optional, List, Dict
import warnings

# Suppress CUDA compatibility warnings for RTX 5090
warnings.filterwarnings("ignore", category=UserWarning, message=".*CUDA capability sm_120.*")

class RTX5090AudioGenerator:
    """
    GPU-Accelerated Audio Generator specifically optimized for RTX 5090
    Uses pure PyTorch tensor operations for maximum GPU utilization
    """
    
    def __init__(self, cache_dir: str = "./rtx5090_audio_cache"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.cache_dir = cache_dir
        self.sample_rate = 44100
        
        print(f"🔥 RTX 5090 Audio Generator initializing...")
        print(f"🎯 Device: {self.device}")
        
        if self.device == "cuda":
            print(f"⚡ GPU: {torch.cuda.get_device_name(0)}")
            print(f"💾 GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
            
            # Optimize RTX 5090 settings
            torch.backends.cudnn.benchmark = True
            torch.backends.cudnn.deterministic = False
            
            # Test GPU functionality
            try:
                test_tensor = torch.randn(1000, 1000, device=self.device)
                _ = torch.mm(test_tensor, test_tensor)
                print("🚀 RTX 5090 tensor operations: WORKING!")
            except Exception as e:
                print(f"❌ GPU test failed: {e}")
                self.device = "cpu"
        
        os.makedirs(cache_dir, exist_ok=True)
        
        # Sound type classification
        self.sound_types = {
            'tavern': 0, 'fire': 1, 'water': 2, 'wind': 3, 'forest': 4,
            'footsteps': 5, 'magic': 6, 'combat': 7, 'ambient': 8,
            'dungeon': 9, 'thunder': 10, 'bell': 11, 'voice': 12,
            'mechanical': 13, 'animal': 14, 'unknown': 15
        }
        
        print(f"✅ RTX 5090 Audio Generator ready!")
    
    def _classify_prompt(self, prompt: str) -> str:
        """Classify prompt to determine sound type."""
        prompt_lower = prompt.lower()
        
        # Direct keyword matching
        for sound_type in self.sound_types:
            if sound_type in prompt_lower:
                return sound_type
        
        # Semantic matching
        if any(word in prompt_lower for word in ['cozy', 'warm', 'inn', 'pub', 'drinking', 'ale', 'beer']):
            return 'tavern'
        elif any(word in prompt_lower for word in ['flame', 'crackling', 'hearth', 'bonfire']):
            return 'fire'
        elif any(word in prompt_lower for word in ['stream', 'river', 'rain', 'drops', 'splash']):
            return 'water'
        elif any(word in prompt_lower for word in ['breeze', 'gust', 'howling', 'rustling']):
            return 'wind'
        elif any(word in prompt_lower for word in ['trees', 'woods', 'nature', 'wilderness', 'leaves']):
            return 'forest'
        elif any(word in prompt_lower for word in ['step', 'walk', 'boot', 'march']):
            return 'footsteps'
        elif any(word in prompt_lower for word in ['spell', 'mystical', 'enchanted', 'arcane', 'shimmer']):
            return 'magic'
        elif any(word in prompt_lower for word in ['sword', 'metal', 'clash', 'battle', 'fight']):
            return 'combat'
        elif any(word in prompt_lower for word in ['cave', 'underground', 'damp', 'echo']):
            return 'dungeon'
        elif any(word in prompt_lower for word in ['storm', 'rumble', 'lightning']):
            return 'thunder'
        elif any(word in prompt_lower for word in ['chime', 'toll', 'ring']):
            return 'bell'
        elif any(word in prompt_lower for word in ['whisper', 'voice', 'speak', 'call']):
            return 'voice'
        elif any(word in prompt_lower for word in ['gear', 'machine', 'click', 'mechanical']):
            return 'mechanical'
        elif any(word in prompt_lower for word in ['bird', 'owl', 'howl', 'roar', 'chirp']):
            return 'animal'
        else:
            return 'ambient'
    
    def _generate_gpu_tavern(self, duration: float) -> torch.Tensor:
        """Generate tavern sounds using GPU tensor operations."""
        samples = int(duration * self.sample_rate)
        
        # Base ambient noise using GPU
        base = torch.randn(samples, device=self.device) * 0.2
        
        # Add fireplace crackling using GPU spectral operations
        crackle_freq = torch.linspace(600, 1200, samples, device=self.device)
        t = torch.linspace(0, duration, samples, device=self.device)
        
        # Multiple crackle layers
        crackles = torch.zeros(samples, device=self.device)
        for i in range(5):
            start_idx = torch.randint(0, samples//2, (1,), device=self.device).item()
            length = torch.randint(samples//20, samples//5, (1,), device=self.device).item()
            end_idx = min(start_idx + length, samples)
            
            # Generate crackle burst on GPU
            burst_t = t[start_idx:end_idx]
            freq = 800 + 400 * torch.sin(2 * torch.pi * 15 * burst_t)
            envelope = torch.exp(-burst_t * 8)
            burst = torch.sin(2 * torch.pi * freq * burst_t) * envelope * 0.3
            
            crackles[start_idx:end_idx] += burst
        
        # Combine on GPU
        audio = base + crackles
        return self._normalize_gpu_audio(audio)
    
    def _generate_gpu_fire(self, duration: float) -> torch.Tensor:
        """Generate fire sounds using GPU tensor operations."""
        samples = int(duration * self.sample_rate)
        t = torch.linspace(0, duration, samples, device=self.device)
        
        # High-frequency crackling base
        fire_base = torch.randn(samples, device=self.device) * 0.3
        
        # Add periodic crackle bursts
        for i in range(int(duration * 4)):
            start = torch.randint(0, samples//2, (1,), device=self.device).item()
            length = torch.randint(samples//50, samples//10, (1,), device=self.device).item()
            end = min(start + length, samples)
            
            # GPU-generated crackle
            burst_t = t[start:end]
            freq = 700 + 300 * torch.cos(2 * torch.pi * 12 * burst_t)
            envelope = torch.exp(-burst_t * 10) 
            burst = torch.sin(2 * torch.pi * freq * burst_t) * envelope * 0.5
            
            fire_base[start:end] += burst
        
        return self._normalize_gpu_audio(fire_base)
    
    def _generate_gpu_water(self, duration: float) -> torch.Tensor:
        """Generate water sounds using GPU tensor operations."""
        samples = int(duration * self.sample_rate)
        t = torch.linspace(0, duration, samples, device=self.device)
        
        # High-frequency water texture
        water_base = torch.randn(samples, device=self.device) * 0.4
        # Simple high-pass filter using GPU
        water_base = torch.diff(water_base, prepend=water_base[0:1])
        
        # Add droplet sounds
        for i in range(int(duration * 3)):
            start = torch.randint(0, samples//2, (1,), device=self.device).item()
            length = torch.randint(samples//100, samples//20, (1,), device=self.device).item()
            end = min(start + length, samples)
            
            # GPU droplet generation
            drop_t = t[start:end]
            freq = 1500 + 500 * torch.sin(2 * torch.pi * 8 * drop_t)
            envelope = torch.exp(-drop_t * 15)
            droplet = torch.sin(2 * torch.pi * freq * drop_t) * envelope * 0.4
            
            water_base[start:end] += droplet
        
        return self._normalize_gpu_audio(water_base)
    
    def _generate_gpu_magic(self, duration: float) -> torch.Tensor:
        """Generate magical sounds using GPU tensor operations."""
        samples = int(duration * self.sample_rate)
        t = torch.linspace(0, duration, samples, device=self.device)
        
        # Shimmering magic base
        magic = torch.zeros(samples, device=self.device)
        
        # Multiple harmonic layers
        for i in range(4):
            freq = 1000 + i * 300
            mod_freq = 5 + i * 2
            
            # Frequency modulation for shimmer
            freq_mod = freq + 100 * torch.sin(2 * torch.pi * mod_freq * t)
            wave = torch.sin(2 * torch.pi * freq_mod * t)
            envelope = torch.exp(-t / (duration * 0.8))
            
            magic += wave * envelope * 0.2
        
        # Add sparkle effects
        for i in range(int(duration * 8)):
            start = torch.randint(0, samples//2, (1,), device=self.device).item()
            length = torch.randint(samples//200, samples//50, (1,), device=self.device).item()
            end = min(start + length, samples)
            
            sparkle_t = t[start:end]
            freq = 1800 + 700 * torch.rand(1, device=self.device).item()
            envelope = torch.exp(-sparkle_t * 20)
            sparkle = torch.sin(2 * torch.pi * freq * sparkle_t) * envelope * 0.3
            
            magic[start:end] += sparkle
        
        return self._normalize_gpu_audio(magic)
    
    def _generate_gpu_combat(self, duration: float) -> torch.Tensor:
        """Generate combat sounds using GPU tensor operations."""
        samples = int(duration * self.sample_rate)
        t = torch.linspace(0, duration, samples, device=self.device)
        
        # Combat base
        combat = torch.randn(samples, device=self.device) * 0.2
        
        # Add metal clashing
        for i in range(int(duration * 2)):
            start = torch.randint(0, samples//2, (1,), device=self.device).item()
            length = torch.randint(samples//20, samples//8, (1,), device=self.device).item()
            end = min(start + length, samples)
            
            clash_t = t[start:end]
            
            # Multi-frequency metal clash
            clash = torch.zeros(len(clash_t), device=self.device)
            for freq in [800, 1200, 1600]:
                wave = torch.sin(2 * torch.pi * freq * clash_t)
                clash += wave * 0.3
            
            envelope = torch.exp(-clash_t * 8)
            combat[start:end] += clash * envelope * 0.6
        
        return self._normalize_gpu_audio(combat)
    
    def _generate_gpu_generic(self, sound_type: str, duration: float) -> torch.Tensor:
        """Generate generic sound using GPU operations."""
        samples = int(duration * self.sample_rate)
        
        # Base noise generation on GPU
        audio = torch.randn(samples, device=self.device) * 0.3
        
        # Apply different filters based on sound type
        if sound_type in ['wind', 'forest', 'ambient']:
            # Low-pass effect
            alpha = 0.1
            filtered = torch.zeros_like(audio)
            filtered[0] = audio[0]
            for i in range(1, len(audio)):
                filtered[i] = alpha * audio[i] + (1 - alpha) * filtered[i-1]
            audio = filtered
        
        elif sound_type in ['bell', 'voice']:
            # Add harmonic content
            t = torch.linspace(0, duration, samples, device=self.device)
            freq = 400 if sound_type == 'bell' else 200
            harmonic = torch.sin(2 * torch.pi * freq * t) * 0.2
            envelope = torch.exp(-t / (duration * 0.5))
            audio += harmonic * envelope
        
        return self._normalize_gpu_audio(audio)
    
    def _normalize_gpu_audio(self, audio: torch.Tensor) -> torch.Tensor:
        """Normalize audio tensor on GPU."""
        # Normalize to [-0.8, 0.8] range
        max_val = torch.max(torch.abs(audio))
        if max_val > 0:
            audio = audio / max_val * 0.8
        
        # Apply fade in/out on GPU
        fade_samples = int(0.05 * self.sample_rate)
        if len(audio) > 2 * fade_samples:
            fade_in = torch.linspace(0, 1, fade_samples, device=self.device)
            fade_out = torch.linspace(1, 0, fade_samples, device=self.device)
            
            audio[:fade_samples] *= fade_in
            audio[-fade_samples:] *= fade_out
        
        return audio
    
    def generate_sound(self, prompt: str, duration: float = 3.0) -> Optional[str]:
        """Generate audio using RTX 5090 GPU acceleration."""
        start_time = time.time()
        
        # Classify sound type
        sound_type = self._classify_prompt(prompt)
        
        # Check cache
        cache_key = hashlib.md5(f"{prompt}_{duration}_{sound_type}".encode()).hexdigest()
        cache_path = os.path.join(self.cache_dir, f"{cache_key}.wav")
        
        if os.path.exists(cache_path):
            print(f"⚡ Cached: '{prompt}' -> {sound_type} ({time.time() - start_time:.3f}s)")
            return cache_path
        
        print(f"🚀 RTX 5090 Generating: '{prompt}' -> {sound_type}")
        
        try:
            # Generate audio using GPU-optimized methods
            if sound_type == 'tavern':
                audio_tensor = self._generate_gpu_tavern(duration)
            elif sound_type == 'fire':
                audio_tensor = self._generate_gpu_fire(duration)
            elif sound_type == 'water':
                audio_tensor = self._generate_gpu_water(duration)
            elif sound_type == 'magic':
                audio_tensor = self._generate_gpu_magic(duration)
            elif sound_type == 'combat':
                audio_tensor = self._generate_gpu_combat(duration)
            else:
                audio_tensor = self._generate_gpu_generic(sound_type, duration)
            
            # Convert to numpy for saving
            audio_np = audio_tensor.detach().cpu().numpy()
            
            # Save to cache
            sf.write(cache_path, audio_np, self.sample_rate)
            
            generation_time = time.time() - start_time
            gpu_memory = torch.cuda.memory_allocated(0) / 1e6 if self.device == "cuda" else 0
            
            print(f"🎉 RTX 5090 generation complete in {generation_time:.4f}s")
            print(f"🎯 GPU Memory: {gpu_memory:.1f} MB")
            
            return cache_path
            
        except Exception as e:
            print(f"❌ RTX 5090 generation failed: {e}")
            return None
    
    def get_cache_info(self) -> Dict:
        """Get cache information."""
        if not os.path.exists(self.cache_dir):
            return {"files": 0, "size_mb": 0}
        
        files = [f for f in os.listdir(self.cache_dir) if f.endswith('.wav')]
        total_size = sum(os.path.getsize(os.path.join(self.cache_dir, f)) for f in files)
        
        return {
            "files": len(files),
            "size_mb": total_size / (1024 * 1024)
        }
    
    def clear_cache(self):
        """Clear the audio cache."""
        import shutil
        if os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)
            os.makedirs(self.cache_dir, exist_ok=True)
        print("🗑️ RTX 5090 audio cache cleared")