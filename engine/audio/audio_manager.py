import pygame
import os

class AudioManager:
    def __init__(self, base_path="assets/sounds"):
        # Initialize mixer
        pygame.mixer.init()

        self.base_path = base_path
        self.sounds = {}

        # Optional: increase channels so multiple sounds can overlap
        pygame.mixer.set_num_channels(16)

    def load_sound(self, name, filename, volume=1.0):
        """Load a sound effect and store it with a key."""
        path = os.path.join(self.base_path, filename)

        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(volume)
            self.sounds[name] = sound
        except Exception as e:
            print(f"Error loading sound {filename}: {e}")

    def play(self, name):
        """Play a loaded sound."""
        if name in self.sounds:
            self.sounds[name].play()

    def stop(self, name):
        """Stop a specific sound."""
        if name in self.sounds:
            self.sounds[name].stop()

    def play_music(self, filename, volume=0.5, loop=True):
        """Play background music."""
        path = os.path.join(self.base_path, filename)

        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1 if loop else 0)
        except Exception as e:
            print(f"Error loading music {filename}: {e}")

    def stop_music(self):
        """Stop background music."""
        pygame.mixer.music.stop()