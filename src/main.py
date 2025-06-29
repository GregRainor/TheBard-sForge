import sys
import time
import select
from audio_engine import AudioEngine
from orchestrator import Orchestrator

if __name__ == "__main__":
    print("RPG Ambiance - V0.2 Smart Orchestrator")
    print("Initializing audio engine...")

    audio_engine = AudioEngine()
    orchestrator = Orchestrator(audio_engine)

    # Load scenes
    if not orchestrator.load_scenes_from_file("scenes.json"):
        print("Fatal: Could not load scenes.json. Exiting.")
        audio_engine.quit()
        sys.exit(1)

    print("Available scenes:", orchestrator.get_available_scenes())
    print("Controls:")
    print("  't' - Switch to tavern scene")
    print("  'f' - Switch to forest scene") 
    print("  's' - Stop current scene")
    print("  'q' - Quit")

    # Start with tavern scene
    print("\nStarting tavern scene...")
    if not orchestrator.play_scene("tavern"):
        print("Warning: Could not start tavern scene")

    print("\nOrchestrator running... (press Enter to see controls)")

    try:
        while True:
            # Update orchestrator for random one-shots
            orchestrator.update()
            
            # Non-blocking input check            
            if select.select([sys.stdin], [], [], 0.1)[0]:
                user_input = input("> ").lower().strip()
                
                if user_input == 't':
                    print("Switching to tavern scene...")
                    orchestrator.play_scene("tavern")
                elif user_input == 'f':
                    print("Switching to forest scene...")
                    orchestrator.play_scene("forest")
                elif user_input == 's':
                    print("Stopping current scene...")
                    orchestrator.stop_current_scene()
                elif user_input == 'q':
                    break
                elif user_input == '':
                    print("Controls: 't'=tavern, 'f'=forest, 's'=stop, 'q'=quit")
                else:
                    print("Unknown command. Use 't', 'f', 's', or 'q'.")
            
            # Small sleep to prevent 100% CPU usage
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    finally:
        print("Stopping all sounds and exiting...")
        orchestrator.stop_current_scene()
        audio_engine.quit()