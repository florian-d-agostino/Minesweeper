import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import arcade
from src.frontend.ShowGrid import ShowGrid
from src.frontend.GetClick import GetClick
from src.frontend.SetMarker import SetMarker
from src.frontend.ShowTimer import ShowTimer
from src.backend.GenerateMap import GenerateMap
from src.backend.RecordManager import RecordManager

class SetGameView(arcade.View):
    def __init__(self, level_id):
        super().__init__()
        self.level_id = level_id
        self.game_map = None  # Generated on first click

        # Background mapping: Easy=bg3, Medium=bg2, Hard=bg1
        bg_map = {1: 3, 2: 2, 3: 1}
        bg_index = bg_map.get(self.level_id, self.level_id)
        bg_path = f"src/public/img/assets/bg-cyber{bg_index}.png"
        try:
            self.background = arcade.load_texture(bg_path)
        except Exception as e:
            print(f"Error loading background {bg_path}: {e}")
            self.background = arcade.load_texture("src/public/img/assets/bg.jpg")

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.show_grid = ShowGrid(self.level_id, self.window.width, self.window.height)
        self.get_click = GetClick(self.show_grid)
        self.set_marker = SetMarker(self.show_grid, self.get_click)
        self.show_timer = ShowTimer(self.window.width - 120, self.window.height - 60)
        self.game_map = None
        self.game_over = False
        self.lost = False
        self.is_record = False

        if hasattr(self, 'background') and self.background:
            self.bg_sprite = arcade.Sprite(self.background)
            self.bg_sprite.center_x = self.window.width / 2
            self.bg_sprite.center_y = self.window.height / 2
            self.bg_sprite.width = self.window.width
            self.bg_sprite.height = self.window.height
            self.bg_sprite_list = arcade.SpriteList()
            self.bg_sprite_list.append(self.bg_sprite)

    def on_draw(self):
        self.clear()

        if hasattr(self, 'bg_sprite_list'):
            self.bg_sprite_list.draw()

        if hasattr(self, 'show_grid'):
            grid = self.game_map.get_map() if self.game_map else None
            self.show_grid.draw(grid)
            self.set_marker.draw_markers(
                grid,
                self.show_grid.cell_data,
                self.show_grid.cell_width,
                self.show_grid.cell_height
            )

        if hasattr(self, 'show_timer'):
            self.show_timer.draw()

        if self.game_over:
            self._draw_game_over_overlay()

    def _draw_game_over_overlay(self):
        # Semi-transparent background
        arcade.draw_rect_filled(
            arcade.LBWH(0, 0, self.window.width, self.window.height),
            (0, 0, 0, 180)
        )

        title = "GAME OVER" if self.lost else "VICTORY!"
        color = arcade.color.RED if self.lost else arcade.color.GREEN

        arcade.draw_text(
            title,
            self.window.width / 2,
            self.window.height / 2 + 100,
            color,
            font_size=50,
            anchor_x="center",
            font_name="Orbitron"
        )

        final_time = self.show_timer.get_formatted_time()
        arcade.draw_text(
            f"Final Time: {final_time}",
            self.window.width / 2,
            self.window.height / 2 + 20,
            arcade.color.CYAN,
            font_size=30,
            anchor_x="center",
            font_name="Orbitron"
        )

        if self.is_record:
            arcade.draw_text(
                "NEW RECORD!",
                self.window.width / 2,
                self.window.height / 2 - 30,
                arcade.color.GOLD,
                font_size=24,
                anchor_x="center",
                font_name="Orbitron",
                bold=True
            )

        # Buttons
        self._draw_button("RESTART", self.window.width / 2 - 120, self.window.height / 2 - 80)
        self._draw_button("MENU", self.window.width / 2 + 120, self.window.height / 2 - 80)

    def _draw_button(self, text, x, y):
        arcade.draw_rect_outline(
            arcade.LBWH(x - 90, y - 25, 180, 50),
            arcade.color.CYAN,
            border_width=2
        )
        arcade.draw_text(
            text,
            x, y,
            arcade.color.CYAN,
            font_size=20,
            anchor_x="center",
            anchor_y="center",
            font_name="Orbitron"
        )

    def on_mouse_press(self, x, y, button, modifiers):
        if self.game_over:
            # Check buttons
            if button == arcade.MOUSE_BUTTON_LEFT:
                # Restart Button
                if abs(x - (self.window.width / 2 - 120)) < 90 and abs(y - (self.window.height / 2 - 80)) < 25:
                    self.on_show_view()
                # Menu Button
                elif abs(x - (self.window.width / 2 + 120)) < 90 and abs(y - (self.window.height / 2 - 80)) < 25:
                    from src.frontend.Menu import Menu
                    menu_view = Menu()
                    self.window.show_view(menu_view)
            return

        col, row = self.get_click.get_col_row(x, y)
        if col is None:
            return

        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.game_map is None:
                # First click: generate the map and start timer
                self.game_map = GenerateMap(self.level_id, [col, row])
                self.show_timer.start()
                # Check for victory even on first click (though unlikely)
                if self.game_map.check_victory():
                    self.game_over = True
                    self.lost = False
                    current_time = self.show_timer.timer.get_time()
                    self.is_record = RecordManager.update_record(self.level_id, current_time)
                    self.show_timer.stop()
            else:
                hit_bomb = self.game_map.reveal_cells(col, row)
                if hit_bomb:
                    self.game_over = True
                    self.lost = True
                    self.show_timer.stop()
                elif self.game_map.check_victory():
                    self.game_over = True
                    self.lost = False
                    current_time = self.show_timer.timer.get_time()
                    self.is_record = RecordManager.update_record(self.level_id, current_time)
                    self.show_timer.stop()

        elif button == arcade.MOUSE_BUTTON_RIGHT:
            self.set_marker.handle_right_click(x, y, self.game_map.get_map() if self.game_map else None)

    def on_hide_view(self):
        if hasattr(self, 'show_timer'):
            self.show_timer.stop()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            from src.frontend.Menu import Menu
            menu_view = Menu()
            self.window.show_view(menu_view)
