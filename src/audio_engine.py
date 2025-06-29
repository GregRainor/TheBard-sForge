import pygame


class AudioEngine:
    def __init__(self):
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.mixer.init()
        pygame.mixer.set_num_channels(16)
        self.channels = []
    
    def play_sound(self, filepath, loop=False, volume=1.0):
        try:
            sound = pygame.mixer.Sound(filepath)
            sound.set_volume(volume)
            
            channel = pygame.mixer.find_channel()
            if channel is None:
                channel = pygame.mixer.Channel(0)
            
            loops = -1 if loop else 0
            channel.play(sound, loops=loops)
            return channel
        except pygame.error as e:
            print(f"Error playing sound {filepath}: {e}")
            return None
    
    def stop_all_sounds(self):
        pygame.mixer.stop()
    
    def quit(self):
        pygame.mixer.quit()