#!/usr/bin/env python3

import sys
import os
sys.path.append('src')

from bards_forge_main import BardsForgeApplication

def test_app_initialization():
    """Test that the app can initialize without errors."""
    print("🔥 TESTING THE BARD'S FORGE APPLICATION")
    print("=" * 50)
    
    try:
        app = BardsForgeApplication()
        print("✅ Application initialized successfully!")
        
        # Test banner display
        print("\n🎭 Testing banner display...")
        app.print_main_banner()
        
        # Test about display  
        print("\n📖 Testing about section...")
        app.show_about()
        
        print("\n✅ Application test complete!")
        
    except Exception as e:
        print(f"❌ Application test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_app_initialization()