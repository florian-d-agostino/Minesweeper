class Game:
    def __init__(self):
        self.game_is_running = True
        self.is_won = False
        self.is_lost = False
        self.difficulty = 0

    def stop_game(self):
        self.game_is_running = False

    # Set the difficulty
    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
    
    # Win / Lose Check
    def win(self):
        self.is_won = True
        self.stop_game()
    
    def lose(self):
        self.is_lost = True
        self.stop_game()
