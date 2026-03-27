import arcade

class MusicManager:
    _instance = None
    
    def __init__(self):
        self.music = None
        self.music_player = None
        self.current_song = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = MusicManager()
        return cls._instance

    def play_music(self, file_path, volume=0.5):
        if self.current_song == file_path and self.music_player and self.music_player.playing:
            return  # Already playing this song
            
        if self.music_player:
            self.stop_music()
            
        self.current_song = file_path
        self.music = arcade.load_sound(file_path)
        self.music_player = self.music.play(loop=True, volume=volume)

    def stop_music(self):
        if self.music and self.music_player:
            self.music.stop(self.music_player)
            self.music_player = None
            self.current_song = None
