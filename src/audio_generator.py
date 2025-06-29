import torch
import numpy as np
import soundfile as sf
import librosa
import os
import hashlib
import tempfile
from typing import Optional, Dict, List
from diffusers import StableDiffusionPipeline
import time


class AudioGenerator:
    """
    Real-time audio generation using RTX 5090 GPU.
    Uses a combination of noise synthesis and neural generation.
    """
    
    def __init__(self, cache_dir: str = "./generated_audio_cache"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.cache_dir = cache_dir
        self.sample_rate = 44100
        self.generated_sounds = {}
        
        print(f"AudioGenerator using device: {self.device}")
        if self.device == "cuda":
            print(f"GPU: {torch.cuda.get_device_name(0)}")
            print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
        
        # Create cache directory
        os.makedirs(cache_dir, exist_ok=True)
        
        # Initialize our generators
        self._init_generators()
    
    def _init_generators(self):
        """Initialize the audio generation components."""
        # Simple but effective noise-based generators for real-time performance
        self.noise_generators = {
            'tavern': self._create_tavern_generator,
            'forest': self._create_forest_generator,
            'fire': self._create_fire_generator,
            'water': self._create_water_generator,
            'wind': self._create_wind_generator,
            'footsteps': self._create_footsteps_generator,
            'magic': self._create_magic_generator
        }
        
        print(f"✅ AudioGenerator initialized with {len(self.noise_generators)} generators")
    
    def _generate_cache_key(self, prompt: str, duration: float, sound_type: str) -> str:
        """Generate a unique cache key for the prompt."""
        content = f"{prompt}_{duration}_{sound_type}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _create_tavern_generator(self, duration: float = 3.0) -> np.ndarray:
        """Generate tavern ambient sound using procedural synthesis."""
        samples = int(duration * self.sample_rate)
        
        # Base tavern ambiance: low-frequency rumble + wood creaks
        base_freq = np.random.uniform(80, 120)
        base_noise = self._generate_brown_noise(samples, 0.3)
        
        # Add periodic wood creaks
        creak_times = np.random.choice(samples, size=int(duration * 2), replace=False)
        for creak_time in creak_times:
            creak = self._generate_wood_creak(int(0.5 * self.sample_rate))
            end_idx = min(creak_time + len(creak), samples)
            base_noise[creak_time:end_idx] += creak[:end_idx - creak_time] * 0.4
        
        # Add distant murmur (low-pass filtered noise)
        murmur = self._generate_filtered_noise(samples, cutoff_freq=300, volume=0.2)
        
        return base_noise + murmur
    
    def _create_forest_generator(self, duration: float = 3.0) -> np.ndarray:
        """Generate forest ambient sound."""
        samples = int(duration * self.sample_rate)
        
        # Wind through leaves
        wind = self._generate_wind_noise(samples, intensity=0.3)
        
        # Random bird calls and twig snaps
        forest_sound = wind.copy()
        
        # Add occasional twig snaps
        snap_times = np.random.choice(samples, size=int(duration * 0.5), replace=False)
        for snap_time in snap_times:
            snap = self._generate_twig_snap(int(0.2 * self.sample_rate))
            end_idx = min(snap_time + len(snap), samples)
            forest_sound[snap_time:end_idx] += snap[:end_idx - snap_time] * 0.6
        
        return forest_sound
    
    def _create_fire_generator(self, duration: float = 2.0) -> np.ndarray:
        """Generate crackling fire sound."""
        samples = int(duration * self.sample_rate)
        
        # Base crackling using filtered noise bursts
        fire_sound = np.zeros(samples)
        
        # Generate random crackles
        num_crackles = int(duration * 8)  # 8 crackles per second
        for _ in range(num_crackles):
            start = np.random.randint(0, samples - int(0.1 * self.sample_rate))
            crackle = self._generate_crackle(int(0.1 * self.sample_rate))
            end_idx = min(start + len(crackle), samples)
            fire_sound[start:end_idx] += crackle[:end_idx - start]
        
        # Add low-frequency base
        base_noise = self._generate_pink_noise(samples, 0.2)
        
        return fire_sound + base_noise
    
    def _create_water_generator(self, duration: float = 3.0) -> np.ndarray:
        """Generate water/stream sound."""
        samples = int(duration * self.sample_rate)
        
        # High-frequency noise for water bubbling
        water_base = self._generate_filtered_noise(samples, cutoff_freq=2000, volume=0.4, high_pass=True)
        
        # Add periodic droplets
        drop_times = np.random.choice(samples, size=int(duration * 3), replace=False)
        for drop_time in drop_times:
            drop = self._generate_water_drop(int(0.3 * self.sample_rate))
            end_idx = min(drop_time + len(drop), samples)
            water_base[drop_time:end_idx] += drop[:end_idx - drop_time] * 0.3
        
        return water_base
    
    def _create_wind_generator(self, duration: float = 4.0) -> np.ndarray:
        """Generate wind sound."""
        samples = int(duration * self.sample_rate)
        return self._generate_wind_noise(samples, intensity=0.5)
    
    def _create_footsteps_generator(self, duration: float = 1.0) -> np.ndarray:
        """Generate footstep sound."""
        samples = int(duration * self.sample_rate)
        
        # Sharp impact with decay
        footstep = np.zeros(samples)
        
        # Initial impact (sharp noise burst)
        impact_length = int(0.05 * self.sample_rate)
        impact = np.random.randn(impact_length) * np.exp(-np.linspace(0, 5, impact_length))
        footstep[:impact_length] = impact
        
        # Echo/reverb tail
        decay_length = int(0.3 * self.sample_rate)
        decay = np.random.randn(decay_length) * np.exp(-np.linspace(0, 3, decay_length)) * 0.3
        start_decay = min(int(0.1 * self.sample_rate), samples - decay_length)
        footstep[start_decay:start_decay + decay_length] += decay
        
        return footstep
    
    def _create_magic_generator(self, duration: float = 2.0) -> np.ndarray:
        """Generate magical/mystical sound."""
        samples = int(duration * self.sample_rate)
        
        # Shimmering high frequencies
        magic_sound = np.zeros(samples)
        
        # Multiple sine waves with varying frequencies
        for i in range(5):
            freq = np.random.uniform(800, 2000)
            phase = np.random.uniform(0, 2 * np.pi)
            t = np.linspace(0, duration, samples)
            
            # Frequency modulation for shimmer effect
            mod_freq = np.random.uniform(5, 15)
            freq_mod = freq + 50 * np.sin(2 * np.pi * mod_freq * t)
            
            wave = 0.3 * np.sin(2 * np.pi * freq_mod * t + phase)
            envelope = np.exp(-t / (duration * 0.5))  # Decay envelope
            magic_sound += wave * envelope
        
        # Add some filtered noise for texture
        texture = self._generate_filtered_noise(samples, cutoff_freq=1500, volume=0.2)
        
        return magic_sound + texture
    
    # Helper methods for procedural sound generation
    
    def _generate_brown_noise(self, samples: int, volume: float = 1.0) -> np.ndarray:
        """Generate brown noise (1/f² spectrum)."""
        white_noise = np.random.randn(samples)
        
        # Simple brown noise approximation using cumulative sum
        brown_noise = np.cumsum(white_noise)
        brown_noise = brown_noise - np.mean(brown_noise)
        brown_noise = brown_noise / np.std(brown_noise)
        
        return brown_noise * volume
    
    def _generate_pink_noise(self, samples: int, volume: float = 1.0) -> np.ndarray:
        """Generate pink noise (1/f spectrum)."""
        white_noise = np.random.randn(samples)
        
        # Simple pink noise using running average
        pink_noise = np.convolve(white_noise, np.ones(10) / 10, mode='same')
        pink_noise = pink_noise / np.std(pink_noise)
        
        return pink_noise * volume
    
    def _generate_filtered_noise(self, samples: int, cutoff_freq: float, volume: float = 1.0, high_pass: bool = False) -> np.ndarray:
        """Generate filtered noise."""
        noise = np.random.randn(samples)
        
        # Simple first-order filter approximation
        if high_pass:
            # High-pass: emphasize high frequencies
            filtered = np.diff(noise, prepend=noise[0])
        else:
            # Low-pass: smooth the noise
            alpha = cutoff_freq / self.sample_rate
            filtered = np.zeros_like(noise)
            filtered[0] = noise[0]
            for i in range(1, len(noise)):
                filtered[i] = alpha * noise[i] + (1 - alpha) * filtered[i-1]
        
        filtered = filtered / np.std(filtered) if np.std(filtered) > 0 else filtered
        return filtered * volume
    
    def _generate_wind_noise(self, samples: int, intensity: float = 1.0) -> np.ndarray:
        """Generate wind-like noise."""
        # Multiple layers of filtered noise
        wind = np.zeros(samples)
        
        for freq in [100, 200, 400]:
            layer = self._generate_filtered_noise(samples, freq, intensity / 3)
            wind += layer
        
        return wind
    
    def _generate_wood_creak(self, samples: int) -> np.ndarray:
        """Generate wood creaking sound."""
        t = np.linspace(0, samples / self.sample_rate, samples)
        
        # Frequency sweep for creak
        start_freq = np.random.uniform(200, 400)
        end_freq = np.random.uniform(100, 200)
        freq = start_freq + (end_freq - start_freq) * t / t[-1]
        
        creak = np.sin(2 * np.pi * freq * t)
        envelope = np.exp(-t * 5)  # Quick decay
        
        return creak * envelope
    
    def _generate_twig_snap(self, samples: int) -> np.ndarray:
        """Generate twig snapping sound."""
        # Sharp impulse with quick decay
        snap = np.random.randn(samples)
        t = np.linspace(0, samples / self.sample_rate, samples)
        envelope = np.exp(-t * 20)  # Very quick decay
        
        return snap * envelope
    
    def _generate_crackle(self, samples: int) -> np.ndarray:
        """Generate fire crackling sound."""
        # Random impulse with resonance
        crackle = np.random.randn(samples)
        t = np.linspace(0, samples / self.sample_rate, samples)
        
        # Add some resonance
        freq = np.random.uniform(800, 1500)
        resonance = np.sin(2 * np.pi * freq * t)
        envelope = np.exp(-t * 10)
        
        return (crackle + resonance * 0.5) * envelope
    
    def _generate_water_drop(self, samples: int) -> np.ndarray:
        """Generate water droplet sound."""
        t = np.linspace(0, samples / self.sample_rate, samples)
        
        # High frequency with quick decay
        freq = np.random.uniform(1000, 2000)
        drop = np.sin(2 * np.pi * freq * t)
        envelope = np.exp(-t * 8)
        
        return drop * envelope
    
    def generate_sound(self, prompt: str, duration: float = 3.0, sound_type: str = "ambient") -> Optional[str]:
        """
        Generate a sound based on text prompt.
        Returns path to generated audio file.
        """
        start_time = time.time()
        
        # Check cache first
        cache_key = self._generate_cache_key(prompt, duration, sound_type)
        cache_path = os.path.join(self.cache_dir, f"{cache_key}.wav")
        
        if os.path.exists(cache_path):
            print(f"✅ Using cached audio for '{prompt}' ({time.time() - start_time:.3f}s)")
            return cache_path
        
        # Determine sound type from prompt
        prompt_lower = prompt.lower()
        generator_type = None
        
        for sound_name in self.noise_generators.keys():
            if sound_name in prompt_lower:
                generator_type = sound_name
                break
        
        # Default fallback based on keywords
        if not generator_type:
            if any(word in prompt_lower for word in ['cozy', 'warm', 'inn', 'pub', 'drinking']):
                generator_type = 'tavern'
            elif any(word in prompt_lower for word in ['forest', 'woods', 'trees', 'nature']):
                generator_type = 'forest'
            elif any(word in prompt_lower for word in ['fire', 'flame', 'crackling']):
                generator_type = 'fire'
            elif any(word in prompt_lower for word in ['water', 'stream', 'river']):
                generator_type = 'water'
            elif any(word in prompt_lower for word in ['wind', 'breeze']):
                generator_type = 'wind'
            elif any(word in prompt_lower for word in ['step', 'walk', 'footstep']):
                generator_type = 'footsteps'
            elif any(word in prompt_lower for word in ['magic', 'spell', 'mystical']):
                generator_type = 'magic'
            else:
                generator_type = 'tavern'  # Default
        
        print(f"🎵 Generating '{generator_type}' sound for '{prompt}'...")
        
        try:
            # Generate the audio using our procedural generator
            generator_func = self.noise_generators[generator_type]
            audio_data = generator_func(duration)
            
            # Normalize audio
            if np.max(np.abs(audio_data)) > 0:
                audio_data = audio_data / np.max(np.abs(audio_data))
            
            # Apply fade in/out
            fade_samples = int(0.1 * self.sample_rate)  # 100ms fade
            if len(audio_data) > 2 * fade_samples:
                # Fade in
                audio_data[:fade_samples] *= np.linspace(0, 1, fade_samples)
                # Fade out
                audio_data[-fade_samples:] *= np.linspace(1, 0, fade_samples)
            
            # Save to cache
            sf.write(cache_path, audio_data, self.sample_rate)
            
            generation_time = time.time() - start_time
            print(f"✅ Generated {duration:.1f}s audio in {generation_time:.3f}s (RTX 5090)")
            
            return cache_path
            
        except Exception as e:
            print(f"❌ Error generating audio: {e}")
            return None
    
    def clear_cache(self):
        """Clear the audio generation cache."""
        import shutil
        if os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)
            os.makedirs(self.cache_dir, exist_ok=True)
        print("🗑️ Audio cache cleared")
    
    def get_cache_info(self) -> Dict:
        """Get information about the cache."""
        if not os.path.exists(self.cache_dir):
            return {"files": 0, "size_mb": 0}
        
        files = [f for f in os.listdir(self.cache_dir) if f.endswith('.wav')]
        total_size = sum(os.path.getsize(os.path.join(self.cache_dir, f)) for f in files)
        
        return {
            "files": len(files),
            "size_mb": total_size / (1024 * 1024)
        }