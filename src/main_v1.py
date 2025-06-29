import sys
import time
import select
from audio_engine import AudioEngine
from generative_orchestrator import GenerativeOrchestrator
from nlp_interpreter import NLPInterpreter


def print_banner():
    """Print the V1.0 banner."""
    print("=" * 60)
    print("🎭 RPG AMBIANCE - V1.0: THE GENERATIVE LEAP 🚀")
    print("=" * 60)
    print("✨ Real-time AI audio generation powered by RTX 5090")
    print("🎵 Create any soundscape from text descriptions")
    print("🔄 Hybrid system: Generated + Pre-recorded audio")
    print("=" * 60)


def print_controls():
    """Print available controls."""
    print("\n🎮 CONTROLS:")
    print("  't' - Switch to tavern scene")
    print("  'f' - Switch to forest scene") 
    print("  'd' - Switch to dungeon scene")
    print("  'b' - Switch to battlefield scene")
    print("  'm' - Switch to magical library scene")
    print("  'p' - Describe a scene with text (NLP)")
    print("  'g' - Generate custom scene on-demand")
    print("  'a' - Add dynamic sound to current scene")
    print("  'stats' - Show generation statistics")
    print("  'clear' - Clear generated audio cache")
    print("  's' - Stop current scene")
    print("  'q' - Quit")
    print("=" * 60)


def handle_custom_generation(orchestrator):
    """Handle custom scene generation."""
    print("\n🎭 CUSTOM SCENE GENERATION")
    print("Describe the scene you want to create:")
    print("Examples:")
    print("  - 'bustling market square with vendors calling'")
    print("  - 'spooky haunted mansion with creaking floors'")
    print("  - 'peaceful lakeside with gentle waves'")
    
    description = input("Scene description > ").strip()
    if description:
        print("\nHow long should the background track be? (default: 30s)")
        duration_input = input("Duration (seconds) > ").strip()
        
        try:
            duration = float(duration_input) if duration_input else 30.0
        except ValueError:
            duration = 30.0
        
        print(f"\n🎵 Generating scene: '{description}' ({duration}s)")
        success = orchestrator.generate_scene_on_demand(description, duration)
        
        if success:
            print("✅ Custom scene generated and playing!")
            print("💡 Tip: You can now add dynamic sounds with 'a'")
        else:
            print("❌ Failed to generate custom scene")
    else:
        print("❌ No description provided")


def handle_dynamic_sound(orchestrator):
    """Handle adding dynamic sounds to current scene."""
    if not orchestrator.current_scene:
        print("❌ No active scene. Start a scene first!")
        return
    
    print(f"\n🔊 ADD DYNAMIC SOUND TO: {orchestrator.current_scene}")
    print("Describe the sound you want to add:")
    print("Examples:")
    print("  - 'church bell tolling in distance'")
    print("  - 'cat meowing'")
    print("  - 'thunder rumbling overhead'")
    
    sound_description = input("Sound description > ").strip()
    if sound_description:
        print("How often should this sound occur? (default: occasionally)")
        freq_input = input("Frequency (never/rarely/occasionally/often) > ").strip().lower()
        
        freq_map = {
            "never": 0.0,
            "rarely": 0.01,
            "occasionally": 0.05,
            "often": 0.15,
            "": 0.05  # default
        }
        
        probability = freq_map.get(freq_input, 0.05)
        
        orchestrator.add_dynamic_oneshot(sound_description, probability)
        print(f"✅ Added '{sound_description}' with {freq_input or 'occasional'} frequency")
    else:
        print("❌ No sound description provided")


def main():
    """Main application loop for V1.0."""
    print_banner()
    
    print("🔧 Initializing V1.0 systems...")
    
    # Initialize components
    audio_engine = AudioEngine()
    orchestrator = GenerativeOrchestrator(audio_engine)
    
    print("🧠 Loading NLP interpreter...")
    nlp_interpreter = NLPInterpreter()
    
    # Load scenes (try V2 first, fallback to V1)
    scenes_loaded = False
    for scenes_file in ["scenes_v2.json", "scenes.json"]:
        if orchestrator.load_scenes_from_file(scenes_file):
            scenes_loaded = True
            break
    
    if not scenes_loaded:
        print("❌ Fatal: Could not load any scenes file. Exiting.")
        audio_engine.quit()
        sys.exit(1)
    
    print(f"📋 Available scenes: {orchestrator.get_available_scenes()}")
    
    print_controls()
    
    # Start with tavern scene if available
    if "tavern" in orchestrator.get_available_scenes():
        print("\n🍺 Starting with tavern scene...")
        if orchestrator.play_scene("tavern"):
            print("✅ Tavern scene started!")
        else:
            print("⚠️ Could not start tavern scene")
    
    print("\n🎮 V1.0 ready! (press Enter to see controls)")
    
    try:
        while True:
            # Update orchestrator for dynamic generation
            orchestrator.update()
            
            # Non-blocking input check            
            if select.select([sys.stdin], [], [], 0.1)[0]:
                user_input = input("> ").lower().strip()
                
                if user_input == 't':
                    print("🍺 Switching to tavern scene...")
                    orchestrator.play_scene("tavern")
                    
                elif user_input == 'f':
                    print("🌲 Switching to forest scene...")
                    orchestrator.play_scene("forest")
                    
                elif user_input == 'd':
                    print("🏰 Switching to dungeon scene...")
                    orchestrator.play_scene("dungeon")
                    
                elif user_input == 'b':
                    print("⚔️ Switching to battlefield scene...")
                    orchestrator.play_scene("battlefield")
                    
                elif user_input == 'm':
                    print("📚 Switching to magical library scene...")
                    orchestrator.play_scene("magical_library")
                    
                elif user_input == 'p':
                    print("\n🧠 NLP SCENE INTERPRETATION")
                    print("Describe your scene:")
                    description = input("> ")
                    scene = nlp_interpreter.interpret_prompt(description, orchestrator.scenes)
                    if scene:
                        print(f"🎯 Interpreted as: {scene}")
                        orchestrator.play_scene(scene)
                    else:
                        print("❓ Could not understand scene description.")
                        print(f"Available scenes: {orchestrator.get_available_scenes()}")
                        
                elif user_input == 'g':
                    handle_custom_generation(orchestrator)
                    
                elif user_input == 'a':
                    handle_dynamic_sound(orchestrator)
                    
                elif user_input == 'stats':
                    stats = orchestrator.get_generation_stats()
                    print(f"\n📊 GENERATION STATISTICS:")
                    print(f"  Current scene: {stats['current_scene'] or 'None'}")
                    print(f"  Generation enabled: {stats['generation_enabled']}")
                    print(f"  Cached files: {stats['cache_files']}")
                    print(f"  Cache size: {stats['cache_size_mb']:.1f} MB")
                    
                elif user_input == 'clear':
                    print("🗑️ Clearing generated audio cache...")
                    orchestrator.clear_generated_cache()
                    
                elif user_input == 's':
                    print("🛑 Stopping current scene...")
                    orchestrator.stop_current_scene()
                    
                elif user_input == 'q':
                    break
                    
                elif user_input == '':
                    print_controls()
                    
                else:
                    print(f"❓ Unknown command: '{user_input}'")
                    print("Press Enter to see available controls")
            
            # Small sleep to prevent 100% CPU usage
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\n⚡ Interrupted by user.")
    finally:
        print("\n🔄 Shutting down V1.0...")
        orchestrator.stop_current_scene()
        
        # Show final stats
        stats = orchestrator.get_generation_stats()
        print(f"📊 Final stats: {stats['cache_files']} files, {stats['cache_size_mb']:.1f} MB generated")
        
        audio_engine.quit()
        print("✅ V1.0 shutdown complete. Thanks for using RPG Ambiance!")


if __name__ == "__main__":
    main()