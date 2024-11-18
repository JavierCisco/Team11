import pygame

class Music:
    def __init__(self):
        pygame.mixer.init()
        self.current_track = None

    def load_track(self, track_path):
        self.current_track = track_path
        pygame.mixer.music.load(track_path)

    def play_track(self, start=0, loop=-1):
        if self.current_track:
            pygame.mixer.music.play(loop, start)
        else:
            print("No track loaded! Use load_track() to load a track first.")

    def pause_track(self):
        pygame.mixer.music.pause()

    def resume_track(self):
        pygame.mixer.music.unpause()

    def stop_track(self):
        pygame.mixer.music.stop()

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

    def is_playing(self):
        return pygame.mixer.music.get_busy()
