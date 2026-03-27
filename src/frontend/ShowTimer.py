import threading
import arcade
from src.backend.Timer import Timer

class ShowTimer:
    def __init__(self, x, y, font_size=14):
        self.x = x
        self.y = y
        self.font_size = font_size
        self.timer = Timer()
        self._thread = None
        self.bg_texture = arcade.load_texture("src/public/img/assets/score.png")

    def start(self):
        """Start the timer in a background thread."""
        self.timer.reset_time()
        self._thread = threading.Thread(target=self.timer.start_time, daemon=True)
        self._thread.start()

    def stop(self):
        """Stop the timer."""
        self.timer.stop_time()

    def get_formatted_time(self):
        """Returns elapsed time as MM:SS string."""
        total = self.timer.get_time()
        minutes = total // 60
        seconds = total % 60
        return f"{minutes:02}:{seconds:02}"

    def draw(self):
        # Background panel
        arcade.draw_texture_rect(
            self.bg_texture,
            arcade.LBWH(self.x - 105, self.y - 55, 210, 110)
        )
        # Timer text
        arcade.draw_text(
            self.get_formatted_time(),
            self.x, self.y,
            (0, 255, 255, 230),
            font_size=self.font_size,
            font_name="Orbitron",
            anchor_x="center",
            anchor_y="center",
            bold=True
        )
