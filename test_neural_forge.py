#!/usr/bin/env python3

import sys
import os
import time
sys.path.append('src')

from neural_audio_forge import NeuralAudioForge


def test_neural_generation():
    """Test the neural audio generation system."""
    print("🔥 TESTING THE BARD'S FORGE - NEURAL AUDIO GENERATION")
    print("=" * 70)
    
    forge = NeuralAudioForge()
    
    test_prompts = [
        "cozy tavern ambient background with fireplace",
        "crackling fire in medieval hearth",
        "footsteps on wooden tavern floor",
        "magical spell being cast with sparkles",
        "water dripping in dark dungeon",
        "wind blowing through ancient forest",
        "metal sword clashing in combat",
        "mystical ambient magical energy"
    ]
    
    print(f"🎵 Testing {len(test_prompts)} neural generations...")
    print()
    
    total_audio_duration = 0
    total_generation_time = 0
    successful_generations = 0
    
    for i, prompt in enumerate(test_prompts, 1):
        duration = 3.0
        print(f"🎭 Test {i}/{len(test_prompts)}: '{prompt}'")
        
        start_time = time.time()
        generated_file = forge.generate_sound(prompt, duration)
        generation_time = time.time() - start_time
        
        if generated_file and os.path.exists(generated_file):
            file_size = os.path.getsize(generated_file) / 1024  # KB
            total_audio_duration += duration
            total_generation_time += generation_time
            successful_generations += 1
            
            ratio = duration / generation_time
            print(f"  ✅ Generated in {generation_time:.3f}s ({file_size:.1f} KB)")
            print(f"  🚀 Performance: {ratio:.1f}x real-time")
            print(f"  📁 File: {os.path.basename(generated_file)}")
        else:
            print(f"  ❌ Generation failed")
        
        print()
    
    # Performance summary
    print("=" * 70)
    print("📊 NEURAL FORGE PERFORMANCE SUMMARY")
    print("=" * 70)
    print(f"Successful generations: {successful_generations}/{len(test_prompts)}")
    print(f"Total audio generated: {total_audio_duration:.1f} seconds")
    print(f"Total generation time: {total_generation_time:.3f} seconds")
    
    if successful_generations > 0:
        avg_generation_time = total_generation_time / successful_generations
        overall_ratio = total_audio_duration / total_generation_time
        
        print(f"Average generation time: {avg_generation_time:.3f}s per sound")
        print(f"Overall speed: {overall_ratio:.1f}x real-time")
        
        if overall_ratio > 10:
            print("🎉 EXCELLENT! Neural forge achieving excellent real-time performance!")
        elif overall_ratio > 5:
            print("✅ GREAT! Neural forge performing well for real-time use!")
        elif overall_ratio > 1:
            print("👍 GOOD! Neural forge achieving real-time generation!")
        else:
            print("⚠️ Neural forge needs optimization for real-time use")
    
    # Cache test
    print(f"\n🗄️ CACHE PERFORMANCE TEST")
    print("Testing cache retrieval speed...")
    
    if test_prompts:
        prompt = test_prompts[0]
        start_time = time.time()
        cached_file = forge.generate_sound(prompt, 3.0)
        cache_time = time.time() - start_time
        
        print(f"Cache retrieval: {cache_time:.6f}s")
        if cache_time < 0.01:
            print("🚀 Cache performance: EXCELLENT!")
        else:
            print("👍 Cache performance: Good")
    
    # Final cache info
    cache_info = forge.get_cache_info()
    print(f"\nFinal cache: {cache_info['files']} files, {cache_info['size_mb']:.1f} MB")
    print("=" * 70)
    print("✅ Neural forge test complete!")


if __name__ == "__main__":
    test_neural_generation()