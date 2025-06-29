#!/usr/bin/env python3

import sys
import os
sys.path.append('src')

from simple_bards_forge import RealisticAudioGenerator

def test_realistic_audio():
    """Test the realistic audio generation."""
    print("🔥 TESTING REALISTIC AUDIO GENERATION")
    print("=" * 60)
    
    audio_gen = RealisticAudioGenerator()
    
    # Test scene descriptions
    test_scenes = [
        "A cozy tavern with crackling fireplace and bard music",
        "Dark forest at night with owl sounds and wind",
        "Epic battle with clashing swords and magic spells",
        "Mystical wizard tower with magical energy",
        "Busy medieval marketplace with crowd chatter"
    ]
    
    for i, scene in enumerate(test_scenes, 1):
        print(f"\n🎭 Test {i}/{len(test_scenes)}: {scene}")
        print("-" * 50)
        
        # Generate scene audio
        generated_files = audio_gen.generate_scene_audio(scene, 5.0)
        
        print(f"✅ Generated {len(generated_files)} audio layers:")
        for sound_type, file_path in generated_files.items():
            file_size = os.path.getsize(file_path) / 1024  # KB
            print(f"  📁 {sound_type}: {os.path.basename(file_path)} ({file_size:.1f} KB)")
        
    print(f"\n🎉 Test complete! Check the audio files in:")
    print(f"📁 {os.path.abspath('./realistic_audio_cache')}")
    
    # List all generated files
    cache_dir = "./realistic_audio_cache"
    if os.path.exists(cache_dir):
        files = [f for f in os.listdir(cache_dir) if f.endswith('.wav')]
        print(f"\n📊 Total files generated: {len(files)}")
        total_size = sum(os.path.getsize(os.path.join(cache_dir, f)) for f in files)
        print(f"💾 Total size: {total_size / (1024*1024):.1f} MB")

if __name__ == "__main__":
    test_realistic_audio()