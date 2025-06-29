#!/usr/bin/env python3

import sys
import os
import time
sys.path.append('src')

from neural_audio_forge import NeuralAudioForge, BardsForgeWorkshop

def demo_neural_generation():
    """Demo the neural audio generation capabilities."""
    print("🔥 THE BARD'S FORGE - LIVE DEMO")
    print("=" * 60)
    
    # Initialize the neural forge
    forge = NeuralAudioForge()
    
    # Demo scenarios for different game situations
    demo_scenarios = [
        {
            "scene": "🍺 Cozy Tavern Evening",
            "sounds": [
                "cozy tavern ambiance with crackling fireplace",
                "ale mugs clinking together cheerfully",
                "wooden chair creaking as patron sits down"
            ]
        },
        {
            "scene": "🌲 Mysterious Forest Journey", 
            "sounds": [
                "wind rustling through ancient forest leaves",
                "twig snapping underfoot in dark woods",
                "distant owl hooting in moonlit forest"
            ]
        },
        {
            "scene": "⚔️ Epic Combat Encounter",
            "sounds": [
                "metal sword clashing against armor",
                "magical spell crackling with energy",
                "battle cry echoing across battlefield"
            ]
        },
        {
            "scene": "🏰 Dark Dungeon Exploration",
            "sounds": [
                "water droplets echoing in stone corridors",
                "heavy door creaking open ominously",
                "mysterious whisper in dungeon shadows"
            ]
        }
    ]
    
    print("🎭 Generating immersive RPG soundscapes...")
    print()
    
    for scenario in demo_scenarios:
        print(f"📖 SCENARIO: {scenario['scene']}")
        print("-" * 40)
        
        for sound_desc in scenario['sounds']:
            start_time = time.time()
            file_path = forge.generate_sound(sound_desc, duration=2.5)
            generation_time = time.time() - start_time
            
            if file_path:
                print(f"  ✅ '{sound_desc}' ({generation_time:.3f}s)")
            else:
                print(f"  ❌ '{sound_desc}' FAILED")
        
        print()
    
    # Show cache performance
    cache_info = forge.get_cache_info()
    print(f"🗄️ CACHE: {cache_info['files']} files, {cache_info['size_mb']:.1f} MB")
    
    print()
    print("🎉 DEMO COMPLETE!")
    print("✨ The Bard's Forge is ready for your RPG adventures!")
    print()
    print("🎮 To use The Bard's Forge:")
    print("   python src/bards_forge_main.py")
    print()

def demo_workshop_features():
    """Demo the workshop preparation features."""
    print("🔨 WORKSHOP MODE DEMO")
    print("=" * 40)
    
    workshop = BardsForgeWorkshop()
    
    # Demo sound pack creation
    tavern_pack = [
        "warm tavern fireplace crackling",
        "wooden barrel being rolled across floor",
        "coin purse jingling with gold pieces"
    ]
    
    print("📦 Creating demo tavern sound pack...")
    for sound in tavern_pack:
        result = workshop.neural_forge.generate_sound(sound, 2.0)
        if result:
            print(f"  ✅ {sound}")
        else:
            print(f"  ❌ {sound}")
    
    print("🔨 Workshop demo complete!")
    print()

if __name__ == "__main__":
    demo_neural_generation()
    demo_workshop_features()