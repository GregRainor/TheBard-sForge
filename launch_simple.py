#!/usr/bin/env python3

"""
Simple Bard's Forge Launcher
Scene-Based RPG Audio Generator
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from simple_bards_forge import SimpleBardsForgeGUI
    
    print("🎭 Launching Simple Bard's Forge...")
    print("🎬 Scene-Based RPG Audio Generator")
    print("✨ Just describe your scene and get instant audio!")
    print()
    
    # Create and run the simple GUI
    app = SimpleBardsForgeGUI()
    app.run()
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install required dependencies:")
    print("pip install numpy soundfile pygame")
    
except Exception as e:
    print(f"❌ Application error: {e}")
    import traceback
    traceback.print_exc()