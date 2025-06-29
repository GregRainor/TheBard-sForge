import sys
from audio_engine import AudioEngine

if __name__ == "__main__":
    print("RPG Ambiance - V0.1 Audio Engine")
    print("Initializing audio engine...")

    audio_engine = AudioEngine()

    print("Controls:")
    print("  'c' - Play clinking mugs sound")
    print("  'q' - Quit")
    print("\nStarting tavern ambiance...")

    # Play tavern ambiance on loop
    tavern_channel = audio_engine.play_sound("assets/sounds/tavern_ambiance.wav", loop=True, volume=0.7)
    if tavern_channel is None:
        print("Fatal: Could not load tavern_ambiance.wav. Exiting.")
        audio_engine.quit()
        sys.exit(1)

    print("\nListening for input...")

    try:
        while True:
            # Blocking input is fine for V0.1, will be replaced in V0.2
            user_input = input("> ").lower().strip()

            if user_input == 'c':
                print("Playing clinking mugs...")
                audio_engine.play_sound("assets/sounds/clinking_mugs.wav", volume=0.8)
            elif user_input == 'q':
                break # Exit loop for graceful shutdown
            else:
                print("Unknown command. Use 'c' for clinking mugs or 'q' to quit.")

    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    finally:
        print("Stopping all sounds and exiting...")
        audio_engine.stop_all_sounds()
        audio_engine.quit()