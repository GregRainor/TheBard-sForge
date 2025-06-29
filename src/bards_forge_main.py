import sys
import time
import select
from audio_engine import AudioEngine
from generative_orchestrator import GenerativeOrchestrator
from nlp_interpreter import NLPInterpreter
from neural_audio_forge import NeuralAudioForge
from workshop_interface import WorkshopInterface


class BardsForgeApplication:
    """
    The Bard's Forge - Complete Application
    Workshop Mode + Performance Mode
    """
    
    def __init__(self):
        self.mode = None
        self.audio_engine = None
        self.orchestrator = None
        self.nlp_interpreter = None
        self.neural_forge = None
        
    def print_main_banner(self):
        """Print the main application banner."""
        print("=" * 70)
        print("🎭 THE BARD'S FORGE 🔨")
        print("=" * 70)
        print("⚡ Neural Audio Generation for RPG Game Masters")
        print("🚀 Powered by RTX 5090 Real-Time AI")
        print("🎵 Create immersive soundscapes from text descriptions")
        print("=" * 70)
        print()
        print("Choose your mode:")
        print("  1. 🔨 Workshop Mode (Sound Preparation)")
        print("  2. 🎭 Performance Mode (Live Gaming)")
        print("  3. ❓ About The Bard's Forge")
        print("  4. 🚪 Exit")
        print("=" * 70)
    
    def show_about(self):
        """Show information about The Bard's Forge."""
        print("\n" + "=" * 70)
        print("📖 ABOUT THE BARD'S FORGE")
        print("=" * 70)
        print()
        print("🎯 PURPOSE:")
        print("  The Bard's Forge is an AI-powered soundscape generator")
        print("  designed specifically for tabletop RPG Game Masters.")
        print()
        print("🔨 WORKSHOP MODE:")
        print("  • Prepare sounds before your gaming session")
        print("  • Generate custom sound packs and libraries") 
        print("  • Create campaign-specific audio collections")
        print("  • Batch generate sounds for efficiency")
        print()
        print("🎭 PERFORMANCE MODE:")
        print("  • Real-time sound generation during gameplay")
        print("  • NLP-powered scene interpretation")
        print("  • Dynamic sound mixing and layering")
        print("  • Instant response to text descriptions")
        print()
        print("⚡ NEURAL TECHNOLOGY:")
        print("  • RTX 5090 GPU-accelerated generation")
        print("  • Spectral convolution neural networks")
        print("  • Real-time audio synthesis from text")
        print("  • Smart caching for instant playback")
        print()
        print("🎵 SUPPORTED SOUNDS:")
        print("  • Environmental ambiances (taverns, forests, dungeons)")
        print("  • Sound effects (combat, magic, nature)")
        print("  • Atmospheric elements (weather, crowds, machinery)")
        print("  • Musical elements (instruments, melodies)")
        print()
        print("=" * 70)
        input("Press Enter to continue...")
    
    def run_workshop_mode(self):
        """Run the workshop mode."""
        print("\n🔨 Starting Workshop Mode...")
        
        try:
            workshop = WorkshopInterface()
            workshop.run()
        except KeyboardInterrupt:
            print("\n⚡ Workshop interrupted by user")
        except Exception as e:
            print(f"\n❌ Workshop error: {e}")
    
    def run_performance_mode(self):
        """Run the performance mode."""
        print("\n🎭 Starting Performance Mode...")
        print("🔧 Initializing performance systems...")
        
        try:
            # Initialize components
            self.audio_engine = AudioEngine()
            self.neural_forge = NeuralAudioForge()
            
            # Create neural-powered orchestrator
            self.orchestrator = GenerativeOrchestrator(self.audio_engine)
            # Replace the old audio generator with neural forge
            self.orchestrator.audio_generator = self.neural_forge
            
            print("🧠 Loading NLP interpreter...")
            self.nlp_interpreter = NLPInterpreter()
            
            # Load scenes
            scenes_loaded = False
            for scenes_file in ["scenes_v2.json", "scenes.json"]:
                if self.orchestrator.load_scenes_from_file(scenes_file):
                    scenes_loaded = True
                    break
            
            if not scenes_loaded:
                print("⚠️ Warning: No scenes file found. Generating mode only.")
            
            # Warm up the neural forge
            print("🔥 Warming up neural forge...")
            self.neural_forge.warmup()
            
            self.performance_mode_loop()
            
        except KeyboardInterrupt:
            print("\n⚡ Performance mode interrupted by user")
        except Exception as e:
            print(f"\n❌ Performance mode error: {e}")
        finally:
            if self.audio_engine:
                print("🔄 Shutting down performance mode...")
                self.orchestrator.stop_current_scene()
                self.audio_engine.quit()
    
    def performance_mode_loop(self):
        """Main loop for performance mode."""
        print("\n" + "=" * 70)
        print("🎭 PERFORMANCE MODE - LIVE GAMING")
        print("=" * 70)
        print("🎮 CONTROLS:")
        print("  't' - Switch to tavern scene")
        print("  'f' - Switch to forest scene")
        print("  'd' - Switch to dungeon scene") 
        print("  'b' - Switch to battlefield scene")
        print("  'm' - Switch to magical library scene")
        print("  'p' - Describe scene with NLP")
        print("  'g' - Generate custom scene on-demand")
        print("  'n' - Neural generate single sound")
        print("  'a' - Add dynamic sound to current scene")
        print("  'stats' - Show statistics")
        print("  'clear' - Clear caches")
        print("  's' - Stop current scene")
        print("  'q' - Return to main menu")
        print("=" * 70)
        
        # Start with tavern if available
        available_scenes = self.orchestrator.get_available_scenes()
        if "tavern" in available_scenes:
            print("\n🍺 Starting with tavern scene...")
            self.orchestrator.play_scene("tavern")
        
        print("\n🎮 Performance mode ready! (press Enter to see controls)")
        
        while True:
            # Update orchestrator
            self.orchestrator.update()
            
            # Non-blocking input check
            if select.select([sys.stdin], [], [], 0.1)[0]:
                user_input = input("> ").lower().strip()
                
                if user_input == 't':
                    print("🍺 Switching to tavern scene...")
                    self.orchestrator.play_scene("tavern")
                    
                elif user_input == 'f':
                    print("🌲 Switching to forest scene...")
                    self.orchestrator.play_scene("forest")
                    
                elif user_input == 'd':
                    print("🏰 Switching to dungeon scene...")
                    self.orchestrator.play_scene("dungeon")
                    
                elif user_input == 'b':
                    print("⚔️ Switching to battlefield scene...")
                    self.orchestrator.play_scene("battlefield")
                    
                elif user_input == 'm':
                    print("📚 Switching to magical library scene...")
                    self.orchestrator.play_scene("magical_library")
                    
                elif user_input == 'p':
                    print("\n🧠 NLP SCENE INTERPRETATION")
                    print("Describe your scene:")
                    description = input("> ")
                    scene = self.nlp_interpreter.interpret_prompt(description, self.orchestrator.scenes)
                    if scene:
                        print(f"🎯 Interpreted as: {scene}")
                        self.orchestrator.play_scene(scene)
                    else:
                        print("❓ Scene not recognized. Generating custom scene...")
                        success = self.orchestrator.generate_scene_on_demand(description)
                        if not success:
                            print("❌ Could not generate scene")
                            
                elif user_input == 'g':
                    print("\n🎭 CUSTOM SCENE GENERATION")
                    description = input("Describe the scene > ")
                    if description:
                        try:
                            duration = float(input("Duration (default: 30s) > ") or "30")
                        except ValueError:
                            duration = 30.0
                        self.orchestrator.generate_scene_on_demand(description, duration)
                    
                elif user_input == 'n':
                    print("\n🎵 NEURAL SOUND GENERATION")
                    prompt = input("Describe the sound > ")
                    if prompt:
                        try:
                            duration = float(input("Duration (default: 3s) > ") or "3")
                        except ValueError:
                            duration = 3.0
                        
                        print(f"🔥 Generating: '{prompt}'...")
                        file_path = self.neural_forge.generate_sound(prompt, duration)
                        if file_path:
                            print(f"✅ Generated! Playing sound...")
                            self.audio_engine.play_sound(file_path, volume=0.8)
                        else:
                            print("❌ Generation failed")
                            
                elif user_input == 'a':
                    if not self.orchestrator.current_scene:
                        print("❌ No active scene. Start a scene first!")
                    else:
                        print(f"\n🔊 ADD DYNAMIC SOUND TO: {self.orchestrator.current_scene}")
                        sound_desc = input("Sound description > ")
                        if sound_desc:
                            freq_input = input("Frequency (rarely/occasionally/often) > ").strip().lower()
                            freq_map = {"rarely": 0.01, "occasionally": 0.05, "often": 0.15}
                            prob = freq_map.get(freq_input, 0.05)
                            self.orchestrator.add_dynamic_oneshot(sound_desc, prob)
                            
                elif user_input == 'stats':
                    stats = self.orchestrator.get_generation_stats()
                    cache_info = self.neural_forge.get_cache_info()
                    
                    print(f"\n📊 THE BARD'S FORGE STATISTICS:")
                    print(f"  Current scene: {stats['current_scene'] or 'None'}")
                    print(f"  Generation enabled: {stats['generation_enabled']}")
                    print(f"  Neural cache files: {cache_info['files']}")
                    print(f"  Neural cache size: {cache_info['size_mb']:.1f} MB")
                    
                    try:
                        import torch
                        if torch.cuda.is_available():
                            memory_used = torch.cuda.memory_allocated(0) / 1e9
                            print(f"  GPU memory used: {memory_used:.1f} GB")
                    except Exception as e:
                        print(f"  GPU memory: Error accessing GPU info")
                        
                elif user_input == 'clear':
                    print("🗑️ Clearing caches...")
                    self.orchestrator.clear_generated_cache()
                    self.neural_forge.clear_cache()
                    
                elif user_input == 's':
                    print("🛑 Stopping current scene...")
                    self.orchestrator.stop_current_scene()
                    
                elif user_input == 'q':
                    break
                    
                elif user_input == '':
                    print("Press 'q' to return to main menu, or see controls above")
                    
                else:
                    print(f"❓ Unknown command: '{user_input}'")
            
            # Small sleep to prevent 100% CPU usage
            time.sleep(0.1)
    
    def run(self):
        """Run the main application."""
        while True:
            self.print_main_banner()
            
            choice = input("\nBard's Forge > ").strip()
            
            if choice == "1":
                self.run_workshop_mode()
            elif choice == "2":
                self.run_performance_mode()
            elif choice == "3":
                self.show_about()
            elif choice == "4":
                print("\n🎭 Thank you for using The Bard's Forge!")
                print("⚡ May your campaigns be epic and your sounds immersive!")
                break
            else:
                print("❌ Invalid choice. Please select 1-4.")


if __name__ == "__main__":
    # Import torch here to handle import issues gracefully
    try:
        import torch
        app = BardsForgeApplication()
        app.run()
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("Please install required packages: pip install torch torchaudio")
    except Exception as e:
        print(f"❌ Application error: {e}")
        sys.exit(1)