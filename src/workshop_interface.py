import sys
import time
import os
from typing import Dict, List, Optional
from neural_audio_forge import BardsForgeWorkshop


class WorkshopInterface:
    """
    The Bard's Forge Workshop - Interactive Interface
    For Game Masters to prepare sounds before sessions
    """
    
    def __init__(self):
        self.workshop = BardsForgeWorkshop()
        self.current_project = None
        self.projects = {}
        
    def print_banner(self):
        """Print the workshop banner."""
        print("=" * 70)
        print("🔨 THE BARD'S FORGE - WORKSHOP MODE 🔨")
        print("=" * 70)
        print("⚡ Powered by RTX 5090 Neural Audio Generation")
        print("🎭 Prepare sounds for your RPG campaigns")
        print("🏗️ Build custom sound libraries and packs")
        print("=" * 70)
    
    def print_menu(self):
        """Print the main workshop menu."""
        print("\n🛠️ WORKSHOP MENU:")
        print("  1. Create New Project")
        print("  2. Load Existing Project") 
        print("  3. Generate Single Sound")
        print("  4. Batch Generate Sounds")
        print("  5. Create Sound Pack")
        print("  6. Campaign Sound Preparation")
        print("  7. Workshop Statistics")
        print("  8. Clear Neural Cache")
        print("  9. Performance Test")
        print("  0. Exit to Performance Mode")
        print("=" * 70)
    
    def create_new_project(self):
        """Create a new sound project."""
        print("\n🆕 CREATE NEW PROJECT")
        project_name = input("Project name > ").strip()
        
        if not project_name:
            print("❌ Invalid project name")
            return
        
        if project_name in self.projects:
            print("❌ Project already exists")
            return
        
        description = input("Project description > ").strip()
        
        self.projects[project_name] = {
            "description": description,
            "sounds": {},
            "packs": [],
            "created": time.time()
        }
        
        self.current_project = project_name
        print(f"✅ Project '{project_name}' created")
    
    def generate_single_sound(self):
        """Generate a single sound."""
        print("\n🎵 SINGLE SOUND GENERATION")
        
        prompt = input("Describe the sound > ").strip()
        if not prompt:
            print("❌ No description provided")
            return
        
        try:
            duration = float(input("Duration in seconds (default: 3.0) > ").strip() or "3.0")
        except ValueError:
            duration = 3.0
        
        print(f"\n🔥 Generating: '{prompt}' ({duration}s)")
        
        start_time = time.time()
        file_path = self.workshop.neural_forge.generate_sound(prompt, duration)
        generation_time = time.time() - start_time
        
        if file_path:
            print(f"✅ Generated in {generation_time:.3f}s")
            print(f"📁 Saved to: {file_path}")
            
            # Add to current project if exists
            if self.current_project:
                self.projects[self.current_project]["sounds"][prompt] = file_path
                print(f"📂 Added to project: {self.current_project}")
        else:
            print("❌ Generation failed")
    
    def batch_generate_sounds(self):
        """Generate multiple sounds in batch."""
        print("\n🔥 BATCH SOUND GENERATION")
        print("Enter sound descriptions (one per line, empty line to finish):")
        
        prompts = []
        while True:
            prompt = input(f"Sound {len(prompts) + 1} > ").strip()
            if not prompt:
                break
            prompts.append(prompt)
        
        if not prompts:
            print("❌ No sounds to generate")
            return
        
        try:
            duration = float(input("Duration for all sounds (default: 3.0) > ").strip() or "3.0")
        except ValueError:
            duration = 3.0
        
        print(f"\n🚀 Batch generating {len(prompts)} sounds...")
        
        start_time = time.time()
        results = self.workshop.neural_forge.generate_batch(prompts, duration)
        total_time = time.time() - start_time
        
        successful = sum(1 for r in results if r is not None)
        print(f"\n📊 Batch Results:")
        print(f"✅ Generated: {successful}/{len(prompts)} sounds")
        print(f"⏱️ Total time: {total_time:.3f}s")
        print(f"🚀 Average: {total_time/len(prompts):.3f}s per sound")
        
        # Add to current project
        if self.current_project and successful > 0:
            for prompt, result in zip(prompts, results):
                if result:
                    self.projects[self.current_project]["sounds"][prompt] = result
            print(f"📂 Added {successful} sounds to project: {self.current_project}")
    
    def create_sound_pack(self):
        """Create a themed sound pack."""
        print("\n📦 CREATE SOUND PACK")
        
        pack_name = input("Pack name > ").strip()
        if not pack_name:
            print("❌ Invalid pack name")
            return
        
        print("Pack type:")
        print("  1. Custom (enter descriptions manually)")
        print("  2. Tavern Pack")
        print("  3. Forest Pack") 
        print("  4. Dungeon Pack")
        print("  5. Combat Pack")
        
        choice = input("Choice > ").strip()
        
        if choice == "1":
            print("Enter sound descriptions (empty line to finish):")
            descriptions = []
            while True:
                desc = input(f"Sound {len(descriptions) + 1} > ").strip()
                if not desc:
                    break
                descriptions.append(desc)
        elif choice == "2":
            descriptions = [
                "cozy tavern ambient background",
                "ale mugs clinking together",
                "crackling fireplace warmth",
                "wooden chair creaking",
                "footsteps on wooden floor",
                "distant tavern laughter",
                "coin purse jingling",
                "tavern door opening with bell"
            ]
        elif choice == "3":
            descriptions = [
                "peaceful forest ambient sounds",
                "wind rustling through leaves",
                "twig snapping underfoot",
                "owl hooting in distance",
                "gentle stream flowing",
                "bird calls in forest",
                "leaves crunching underfoot",
                "distant wolf howl"
            ]
        elif choice == "4":
            descriptions = [
                "dark dungeon ambient echoes",
                "water droplets echoing",
                "stone footsteps echoing",
                "distant dungeon rumbling",
                "chain rattling in darkness",
                "door creaking open heavily",
                "torch crackling on wall",
                "mysterious dungeon whisper"
            ]
        elif choice == "5":
            descriptions = [
                "intense battle ambient",
                "metal clashing against metal",
                "armor clanking movement",
                "war horn in distance", 
                "battle cry and shouts",
                "arrows whistling through air",
                "shield blocking impact",
                "sword being unsheathed"
            ]
        else:
            print("❌ Invalid choice")
            return
        
        if not descriptions:
            print("❌ No descriptions provided")
            return
        
        print(f"\n📦 Creating pack '{pack_name}' with {len(descriptions)} sounds...")
        
        pack_dir = self.workshop.create_sound_pack(pack_name, descriptions)
        
        # Add to current project
        if self.current_project:
            self.projects[self.current_project]["packs"].append(pack_dir)
            print(f"📂 Pack added to project: {self.current_project}")
    
    def campaign_preparation(self):
        """Prepare sounds for an entire campaign."""
        print("\n🏰 CAMPAIGN SOUND PREPARATION")
        
        campaign_name = input("Campaign name > ").strip()
        if not campaign_name:
            print("❌ Invalid campaign name")
            return
        
        print("\nSelect campaign style:")
        print("  1. High Fantasy")
        print("  2. Urban Adventure") 
        print("  3. Horror/Gothic")
        print("  4. Sci-Fi")
        print("  5. Custom")
        
        style = input("Style > ").strip()
        
        if style == "1":
            campaign_sounds = {
                "environments": [
                    "medieval tavern atmosphere",
                    "mystical forest ambiance", 
                    "ancient castle halls",
                    "underground dungeon echoes",
                    "magical library whispers"
                ],
                "effects": [
                    "magical spell casting",
                    "sword combat clashing",
                    "dragon roar in distance",
                    "healing potion bubbling",
                    "treasure chest opening"
                ],
                "creatures": [
                    "goblin chittering sounds",
                    "wolf howling at night",
                    "bird of prey screech",
                    "horse galloping hooves",
                    "mystical creature purr"
                ]
            }
        elif style == "2":
            campaign_sounds = {
                "environments": [
                    "busy city street ambiance",
                    "nightclub atmosphere",
                    "office building hum",
                    "subway train sounds",
                    "rooftop wind sounds"
                ],
                "effects": [
                    "car engine starting",
                    "phone ringing urgently", 
                    "keyboard typing rapidly",
                    "footsteps on concrete",
                    "door slamming shut"
                ],
                "technology": [
                    "computer beeping alerts",
                    "radio static crackling",
                    "elevator ding sound",
                    "cash register ringing",
                    "smartphone notification"
                ]
            }
        elif style == "3":
            campaign_sounds = {
                "environments": [
                    "haunted mansion creaking",
                    "foggy graveyard silence",
                    "abandoned hospital echoes",
                    "dark forest at midnight",
                    "storm approaching ominously"
                ],
                "effects": [
                    "ghostly whisper calling",
                    "door slowly creaking open",
                    "floorboard creaking ominously",
                    "wind howling through ruins",
                    "chain dragging on floor"
                ],
                "supernatural": [
                    "spectral wail echoing",
                    "mysterious footsteps above",
                    "candle flame flickering",
                    "book pages turning alone",
                    "clock ticking ominously"
                ]
            }
        elif style == "4":
            campaign_sounds = {
                "environments": [
                    "spaceship engine humming",
                    "alien planet atmosphere",
                    "space station ambiance",
                    "asteroid field silence",
                    "cyberpunk city rain"
                ],
                "technology": [
                    "laser weapon charging",
                    "robot movement servos",
                    "computer terminal beeping",
                    "airlock cycling sound",
                    "hologram activation hum"
                ],
                "vehicles": [
                    "spaceship takeoff thrust",
                    "hover car passing by",
                    "mech suit footsteps",
                    "teleporter activation",
                    "plasma engine ignition"
                ]
            }
        else:
            print("Enter custom categories and sounds...")
            # Custom implementation would go here
            return
        
        print(f"\n🏗️ Preparing {campaign_name} campaign sounds...")
        generated_sounds = self.workshop.prepare_campaign_sounds(campaign_sounds)
        
        # Save campaign to project
        if self.current_project:
            self.projects[self.current_project][f"campaign_{campaign_name}"] = generated_sounds
            print(f"📂 Campaign added to project: {self.current_project}")
    
    def show_statistics(self):
        """Show workshop statistics."""
        cache_info = self.workshop.neural_forge.get_cache_info()
        
        print("\n📊 WORKSHOP STATISTICS")
        print("=" * 40)
        print(f"Neural Cache Files: {cache_info['files']}")
        print(f"Cache Size: {cache_info['size_mb']:.1f} MB")
        print(f"Active Projects: {len(self.projects)}")
        print(f"Current Project: {self.current_project or 'None'}")
        
        if self.current_project and self.current_project in self.projects:
            project = self.projects[self.current_project]
            print(f"\nCurrent Project Details:")
            print(f"  Sounds: {len(project.get('sounds', {}))}")
            print(f"  Packs: {len(project.get('packs', []))}")
            print(f"  Description: {project.get('description', 'None')}")
        
        # GPU memory info
        try:
            import torch
            if torch.cuda.is_available():
                memory_allocated = torch.cuda.memory_allocated(0) / 1e9
                memory_reserved = torch.cuda.memory_reserved(0) / 1e9
                print(f"\nGPU Memory:")
                print(f"  Allocated: {memory_allocated:.1f} GB")
                print(f"  Reserved: {memory_reserved:.1f} GB")
        except ImportError:
            print(f"\nGPU Memory: Not available (torch not imported)")
        except Exception as e:
            print(f"\nGPU Memory: Error accessing GPU info ({e})")
    
    def performance_test(self):
        """Run a performance test on the neural forge."""
        print("\n🚀 NEURAL FORGE PERFORMANCE TEST")
        print("Testing generation speed on RTX 5090...")
        
        test_prompts = [
            "tavern ambient background",
            "crackling fire sounds", 
            "footsteps on stone",
            "magical spell effect",
            "sword combat clash"
        ]
        
        # Warmup
        print("🔥 Warming up neural forge...")
        self.workshop.neural_forge.warmup()
        
        # Performance test
        print("⚡ Running performance test...")
        
        total_audio_time = 0
        total_generation_time = 0
        
        for i, prompt in enumerate(test_prompts):
            duration = 3.0
            print(f"Test {i+1}/{len(test_prompts)}: {prompt}")
            
            start_time = time.time()
            result = self.workshop.neural_forge.generate_sound(prompt, duration)
            generation_time = time.time() - start_time
            
            if result:
                total_audio_time += duration
                total_generation_time += generation_time
                ratio = duration / generation_time
                print(f"  ✅ {generation_time:.3f}s ({ratio:.1f}x real-time)")
            else:
                print(f"  ❌ Failed")
        
        if total_generation_time > 0:
            overall_ratio = total_audio_time / total_generation_time
            print(f"\n📊 PERFORMANCE RESULTS:")
            print(f"Overall Speed: {overall_ratio:.1f}x real-time")
            print(f"Average Generation: {total_generation_time/len(test_prompts):.3f}s")
            
            if overall_ratio > 10:
                print("🎉 EXCELLENT PERFORMANCE!")
            elif overall_ratio > 5:
                print("✅ Great performance")
            else:
                print("⚠️ Consider GPU optimization")
    
    def run(self):
        """Run the workshop interface."""
        self.print_banner()
        
        while True:
            self.print_menu()
            
            choice = input("\nWorkshop > ").strip()
            
            if choice == "1":
                self.create_new_project()
            elif choice == "2":
                # Load project implementation
                print("📂 Project loading not implemented yet")
            elif choice == "3":
                self.generate_single_sound()
            elif choice == "4":
                self.batch_generate_sounds()
            elif choice == "5":
                self.create_sound_pack()
            elif choice == "6":
                self.campaign_preparation()
            elif choice == "7":
                self.show_statistics()
            elif choice == "8":
                self.workshop.neural_forge.clear_cache()
            elif choice == "9":
                self.performance_test()
            elif choice == "0":
                print("🎭 Switching to Performance Mode...")
                break
            else:
                print("❌ Invalid choice")


if __name__ == "__main__":
    # Import torch here to avoid early import
    import torch
    
    workshop = WorkshopInterface()
    workshop.run()