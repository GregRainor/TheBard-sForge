#!/usr/bin/env python3

"""
The Bard's Forge GUI Launcher
RTX 5090 Neural Audio Generator for RPG Game Masters
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from bards_forge_gui import BardsForgeGUI
    
    print("🔥 Launching The Bard's Forge GUI...")
    print("⚡ RTX 5090 Neural Audio Generator")
    print("🎭 Professional interface for RPG Game Masters")
    print()
    
    # Create and run the GUI
    app = BardsForgeGUI()
    app.run()
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure all dependencies are installed:")
    print("pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128")
    print("pip install soundfile numpy pygame transformers")
    
except Exception as e:
    print(f"❌ Application error: {e}")
    import traceback
    traceback.print_exc()