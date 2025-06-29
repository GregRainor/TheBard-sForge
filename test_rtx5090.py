#!/usr/bin/env python3

import sys
import os
import time
import warnings

# Suppress CUDA compatibility warnings for RTX 5090 testing
warnings.filterwarnings("ignore", category=UserWarning, message=".*CUDA capability sm_120.*")

sys.path.append('src')
from neural_audio_forge import NeuralAudioForge

def test_rtx5090_performance():
    """Test RTX 5090 GPU acceleration performance."""
    print("🔥 RTX 5090 GPU ACCELERATION TEST")
    print("=" * 60)
    
    # Test GPU acceleration
    print("🚀 Testing with GPU acceleration...")
    gpu_forge = NeuralAudioForge(force_gpu=True)
    
    print(f"Device in use: {gpu_forge.device}")
    print()
    
    # Warm up GPU
    print("🔥 Warming up RTX 5090...")
    gpu_forge.warmup()
    
    # Performance test prompts
    test_prompts = [
        "crackling tavern fireplace",
        "mystical spell casting", 
        "metal combat clashing",
        "water dripping in cave",
        "wind through forest trees"
    ]
    
    print("⚡ RTX 5090 PERFORMANCE TEST")
    print("-" * 40)
    
    total_gpu_time = 0
    total_audio_duration = 0
    
    for i, prompt in enumerate(test_prompts, 1):
        duration = 3.0
        print(f"Test {i}/{len(test_prompts)}: {prompt}")
        
        start_time = time.time()
        result = gpu_forge.generate_sound(prompt, duration)
        generation_time = time.time() - start_time
        
        if result:
            total_gpu_time += generation_time
            total_audio_duration += duration
            speed = duration / generation_time
            print(f"  ✅ Generated in {generation_time:.4f}s ({speed:.1f}x real-time)")
            
            if gpu_forge.device == "cuda":
                memory_mb = torch.cuda.memory_allocated(0) / 1e6
                print(f"  🎯 GPU Memory: {memory_mb:.1f} MB")
        else:
            print(f"  ❌ Failed")
        print()
    
    # Performance summary
    if total_gpu_time > 0:
        overall_speed = total_audio_duration / total_gpu_time
        avg_time = total_gpu_time / len(test_prompts)
        
        print("📊 RTX 5090 PERFORMANCE RESULTS")
        print("=" * 40)
        print(f"Device used: {gpu_forge.device.upper()}")
        print(f"Overall speed: {overall_speed:.1f}x real-time")
        print(f"Average generation time: {avg_time:.4f}s")
        print(f"Total audio generated: {total_audio_duration:.1f}s")
        print(f"Total generation time: {total_gpu_time:.4f}s")
        
        if gpu_forge.device == "cuda":
            print(f"GPU memory used: {torch.cuda.memory_allocated(0) / 1e6:.1f} MB")
            print(f"GPU memory peak: {torch.cuda.max_memory_allocated(0) / 1e6:.1f} MB")
            
            if overall_speed > 50:
                print("🎉 EXCELLENT RTX 5090 PERFORMANCE!")
            elif overall_speed > 20:
                print("✅ GREAT RTX 5090 PERFORMANCE!")
            else:
                print("👍 GOOD RTX 5090 PERFORMANCE!")
        else:
            print("⚠️ Running on CPU - GPU acceleration failed")
    
    # Cache performance test
    print(f"\n🗄️ CACHE PERFORMANCE TEST")
    cache_prompt = test_prompts[0]
    start_time = time.time()
    cached_result = gpu_forge.generate_sound(cache_prompt, 3.0)
    cache_time = time.time() - start_time
    
    print(f"Cache retrieval: {cache_time:.6f}s")
    if cache_time < 0.001:
        print("🚀 Cache: LIGHTNING FAST!")
    else:
        print("👍 Cache: Good performance")

def test_cpu_comparison():
    """Compare with CPU performance."""
    print(f"\n🔄 CPU COMPARISON TEST")
    print("-" * 30)
    
    cpu_forge = NeuralAudioForge(force_gpu=False)
    
    test_prompt = "tavern fireplace crackling"
    duration = 3.0
    
    start_time = time.time()
    result = cpu_forge.generate_sound(test_prompt, duration)
    cpu_time = time.time() - start_time
    
    if result:
        cpu_speed = duration / cpu_time
        print(f"CPU generation: {cpu_time:.4f}s ({cpu_speed:.1f}x real-time)")
    else:
        print("CPU generation failed")

if __name__ == "__main__":
    import torch
    test_rtx5090_performance()
    test_cpu_comparison()