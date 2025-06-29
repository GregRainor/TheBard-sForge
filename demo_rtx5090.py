#!/usr/bin/env python3

import sys
import time
sys.path.append('src')

from neural_audio_forge import NeuralAudioForge

def demo_rtx5090_neural_generation():
    """Demo the RTX 5090 neural generation capabilities."""
    print("🔥 RTX 5090 NEURAL GENERATION DEMO")
    print("=" * 60)
    
    # Initialize with RTX 5090
    forge = NeuralAudioForge(force_gpu=True)
    
    print()
    print("🎭 DEMO: Epic RPG Soundscapes")
    print("-" * 40)
    
    # Demo scenarios for RPG gaming
    demo_sounds = [
        "epic dragon roar echoing through ancient mountains",
        "mystical wizard casting powerful lightning spell",
        "tavern bard playing lute by crackling fireplace",
        "heavy armored knight walking on stone dungeon floor",
        "magical portal opening with shimmering energy"
    ]
    
    total_generation_time = 0
    total_audio_duration = 0
    
    for i, prompt in enumerate(demo_sounds, 1):
        duration = 3.0
        print(f"\n🎵 Demo {i}/{len(demo_sounds)}: {prompt}")
        
        start_time = time.time()
        result = forge.generate_sound(prompt, duration)
        generation_time = time.time() - start_time
        
        if result:
            total_generation_time += generation_time
            total_audio_duration += duration
            speed_ratio = duration / generation_time
            
            print(f"✅ Generated in {generation_time:.3f}s")
            print(f"🚀 Speed: {speed_ratio:.1f}x real-time")
            print(f"📁 File: {result}")
        else:
            print("❌ Generation failed")
    
    # Performance summary
    if total_generation_time > 0:
        overall_speed = total_audio_duration / total_generation_time
        
        print(f"\n🎉 RTX 5090 NEURAL GENERATION RESULTS")
        print("=" * 50)
        print(f"🎯 Overall Speed: {overall_speed:.1f}x real-time")
        print(f"⚡ Average Time: {total_generation_time/len(demo_sounds):.3f}s per sound")
        print(f"🎵 Total Audio: {total_audio_duration:.1f} seconds")
        print(f"⏱️ Total Time: {total_generation_time:.3f} seconds")
        
        # GPU info
        try:
            import torch
            if torch.cuda.is_available():
                memory_gb = torch.cuda.memory_allocated(0) / 1e9
                print(f"💾 GPU Memory: {memory_gb:.2f} GB")
                print(f"🎯 GPU Device: {torch.cuda.get_device_name(0)}")
        except:
            pass
        
        print()
        if overall_speed > 20:
            print("🎉 EXCELLENT RTX 5090 PERFORMANCE!")
            print("✨ Your neural audio generation is blazing fast!")
        elif overall_speed > 5:
            print("✅ GREAT RTX 5090 PERFORMANCE!")
            print("🚀 Neural generation is working excellently!")
        else:
            print("👍 GOOD RTX 5090 PERFORMANCE!")
    
    # Cache info
    cache_info = forge.get_cache_info()
    print(f"\n📁 Neural Cache: {cache_info['files']} files, {cache_info['size_mb']:.1f} MB")
    
    print("\n🎭 Demo complete! Your RTX 5090 is ready for epic RPG adventures!")
    print()
    print("🎮 To use The Bard's Forge:")
    print("   python launch_gui.py    # Professional GUI")
    print("   python src/bards_forge_main.py    # CLI interface")

if __name__ == "__main__":
    demo_rtx5090_neural_generation()