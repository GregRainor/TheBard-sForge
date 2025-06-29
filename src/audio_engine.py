import pygame
import os


class AudioEngine:
    """Handles loading and playback of audio files using pygame."""

    def __init__(self, num_channels=16):
        """Initializes the pygame mixer."""
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.init() # pygame.mixer.init() is called by pygame.init()
        pygame.mixer.set_num_channels(num_channels)
        self.sound_cache = {}

    def play_sound(self, filepath, loop=False, volume=1.0):
        """Loads and plays a sound on the first available channel."""
        abs_path = os.path.abspath(filepath)
        
        # Check cache first
        sound = self.sound_cache.get(abs_path)
        if sound is None:
            try:
                sound = pygame.mixer.Sound(abs_path)
                self.sound_cache[abs_path] = sound
            except pygame.error as e:
                print(f"Error loading sound {filepath}: {e}")
                return None

        try:
            sound.set_volume(volume)

            channel = pygame.mixer.find_channel(True) # Pass True to force find
            if channel is None:
                print(f"Warning: No free channels to play sound {filepath}")
                return None
            loops = -1 if loop else 0
            channel.play(sound, loops=loops)
            return channel
        except pygame.error as e:
            print(f"Error playing sound {filepath}: {e}")
            return None

    def stop_all_sounds(self):
        """Stops all currently playing sounds."""
        pygame.mixer.stop()

    def quit(self):
        """Quits the pygame mixer."""
        pygame.mixer.quit()