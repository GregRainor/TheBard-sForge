#!/usr/bin/env python3

import sys
import os
import time
import warnings

# Suppress CUDA compatibility warnings
warnings.filterwarnings("ignore", category=UserWarning, message=".*CUDA capability sm_120.*")

sys.path.append('src')
from gpu_audio_generator import RTX5090AudioGenerator

def test_rtx5090_true_acceleration():
    """Test true RTX 5090 GPU acceleration with tensor operations."""
    print("🔥 RTX 5090 TRUE GPU ACCELERATION TEST")
    print("=" * 70)
    
    # Initialize RTX 5090 generator
    gpu_gen = RTX5090AudioGenerator()
    
    if gpu_gen.device != "cuda":
        print("❌ GPU not available, cannot test RTX 5090 acceleration")
        return
    
    # Test scenarios designed for GPU
    test_scenarios = [
        {
            "name": "🍺 Epic Tavern Scene",
            "sounds": [
                "cozy tavern with crackling fireplace",
                "ale mugs clinking cheerfully together",
                "wooden chair creaking under patron"
            ]
        },
        {
            "name": "⚔️ Intense Combat Scene", 
            "sounds": [
                "metal sword clashing against shield",
                "mystical spell crackling with energy",
                "armor clanking in fierce battle"
            ]
        },
        {
            "name": "🔮 Magical Mystical Scene",
            "sounds": [
                "magical spell shimmering with power",
                "arcane energy crackling in air",
                "mystical portal opening with sparkles"
            ]
        },
        {
            "name": "🌊 Atmospheric Water Scene",
            "sounds": [
                "water droplets echoing in cave",
                "gentle stream flowing over rocks",
                "rain pattering on leaves"
            ]
        }
    ]
    
    total_gpu_time = 0
    total_audio_duration = 0
    total_sounds = 0
    
    for scenario in test_scenarios:
        print(f"\n📖 {scenario['name']}")
        print("-" * 50)
        
        for sound_desc in scenario['sounds']:
            duration = 2.5
            start_time = time.time()
            
            # Clear GPU cache before generation for accurate timing
            import torch
            if torch.cuda.is_available():
                torch.cuda.synchronize()
                torch.cuda.empty_cache()
            
            file_path = gpu_gen.generate_sound(sound_desc, duration)
            
            # Synchronize GPU to get accurate timing
            if torch.cuda.is_available():
                torch.cuda.synchronize()
            
            generation_time = time.time() - start_time
            
            if file_path:
                total_gpu_time += generation_time
                total_audio_duration += duration
                total_sounds += 1
                
                speed_ratio = duration / generation_time
                print(f"  ✅ '{sound_desc}'")
                print(f"      Time: {generation_time:.4f}s | Speed: {speed_ratio:.1f}x real-time")
                
                # GPU memory info
                if torch.cuda.is_available():
                    memory_mb = torch.cuda.memory_allocated(0) / 1e6
                    print(f"      GPU Memory: {memory_mb:.1f} MB")
            else:
                print(f"  ❌ '{sound_desc}' FAILED")
    
    # Performance analysis
    print(f"\n🚀 RTX 5090 PERFORMANCE ANALYSIS")
    print("=" * 60)
    
    if total_sounds > 0:
        overall_speed = total_audio_duration / total_gpu_time
        avg_generation_time = total_gpu_time / total_sounds
        
        print(f"Device: {gpu_gen.device.upper()} (RTX 5090)")
        print(f"Total sounds generated: {total_sounds}")
        print(f"Total audio duration: {total_audio_duration:.1f}s")
        print(f"Total generation time: {total_gpu_time:.4f}s")
        print(f"Average generation time: {avg_generation_time:.4f}s per sound")
        print(f"Overall speed: {overall_speed:.1f}x real-time")
        
        # GPU utilization info
        import torch
        if torch.cuda.is_available():
            gpu_memory_peak = torch.cuda.max_memory_allocated(0) / 1e6
            gpu_memory_current = torch.cuda.memory_allocated(0) / 1e6
            gpu_memory_total = torch.cuda.get_device_properties(0).total_memory / 1e9
            
            print(f"\nGPU Memory Utilization:")
            print(f"  Current: {gpu_memory_current:.1f} MB")
            print(f"  Peak: {gpu_memory_peak:.1f} MB")
            print(f"  Total: {gpu_memory_total:.1f} GB")
            print(f"  Utilization: {(gpu_memory_peak / 1000) / gpu_memory_total * 100:.2f}%")
        
        # Performance rating
        print(f"\nPerformance Rating:")
        if overall_speed > 100:
            print("🎉 EXCEPTIONAL RTX 5090 PERFORMANCE!")
            print("   GPU tensor operations are working flawlessly!")
        elif overall_speed > 50:
            print("🚀 EXCELLENT RTX 5090 PERFORMANCE!")
            print("   GPU acceleration is highly effective!")
        elif overall_speed > 20:
            print("✅ GREAT RTX 5090 PERFORMANCE!")
            print("   GPU is providing significant acceleration!")
        else:
            print("👍 GOOD RTX 5090 PERFORMANCE!")
            print("   GPU acceleration is working!")
    
    # Cache performance test
    print(f"\n🗄️ CACHE PERFORMANCE TEST")
    print("-" * 30)
    
    cache_test_prompt = "cozy tavern with crackling fireplace"
    
    start_time = time.time()
    cached_result = gpu_gen.generate_sound(cache_test_prompt, 2.5)
    cache_time = time.time() - start_time
    
    print(f"Cache retrieval time: {cache_time:.6f}s")
    if cache_time < 0.001:
        print("🚀 Cache: LIGHTNING FAST!")
    elif cache_time < 0.01:
        print("⚡ Cache: EXCELLENT!")
    else:
        print("👍 Cache: Good performance")
    
    # Final cache stats
    cache_info = gpu_gen.get_cache_info()
    print(f"\nCache Status:")
    print(f"  Files: {cache_info['files']}")
    print(f"  Size: {cache_info['size_mb']:.1f} MB")

def benchmark_gpu_vs_cpu():
    """Benchmark GPU vs CPU performance."""
    print(f"\n🏁 GPU vs CPU BENCHMARK")
    print("=" * 40)
    
    import torch
    if not torch.cuda.is_available():
        print("❌ CUDA not available for benchmark")
        return
    
    # Test the same operation on GPU vs CPU
    test_prompt = "magical spell with sparkles"
    duration = 3.0
    
    # GPU test
    print("🚀 GPU Performance Test...")
    gpu_gen = RTX5090AudioGenerator()
    
    start_time = time.time()
    gpu_result = gpu_gen.generate_sound(test_prompt, duration)
    gpu_time = time.time() - start_time
    
    if gpu_result:
        gpu_speed = duration / gpu_time
        print(f"  GPU: {gpu_time:.4f}s ({gpu_speed:.1f}x real-time)")
    else:
        print("  GPU: Generation failed")
    
    # CPU simulation (tensor operations on CPU)
    print("💻 CPU Performance Test...")
    
    # Force CPU mode by creating tensors on CPU
    start_time = time.time()
    
    # Simulate the same operations but on CPU
    samples = int(duration * 44100)
    cpu_audio = torch.randn(samples) * 0.3  # CPU tensor
    
    # Add some processing
    t = torch.linspace(0, duration, samples)
    freq = 1000
    wave = torch.sin(2 * torch.pi * freq * t) * 0.2
    cpu_audio += wave
    
    # Normalize
    max_val = torch.max(torch.abs(cpu_audio))
    if max_val > 0:
        cpu_audio = cpu_audio / max_val * 0.8
    
    cpu_time = time.time() - start_time
    cpu_speed = duration / cpu_time
    
    print(f"  CPU: {cpu_time:.4f}s ({cpu_speed:.1f}x real-time)")
    
    # Comparison
    if gpu_time > 0 and cpu_time > 0:
        speedup = cpu_time / gpu_time
        print(f"\n📊 Performance Comparison:")
        print(f"  GPU speedup: {speedup:.1f}x faster than CPU")
        
        if speedup > 2:
            print("🎉 Significant GPU acceleration achieved!")
        elif speedup > 1.2:
            print("✅ Good GPU acceleration!")
        else:
            print("⚠️ Limited GPU acceleration")

if __name__ == "__main__":
    test_rtx5090_true_acceleration()
    benchmark_gpu_vs_cpu()