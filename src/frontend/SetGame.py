import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import arcade
from src.frontend.ShowGrid import ShowGrid

class SetGameView(arcade.View):
    def __init__(self, level_id):
        super().__init__()
        self.level_id = level_id
        
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
        # Initialize or recompute the grid when the view is shown and window bounds are established
        arcade.set_background_color(arcade.color.BLACK)
        self.show_grid = ShowGrid(self.level_id, self.window.width, self.window.height)
        
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
        
        # Draw background via sprite list
        if hasattr(self, 'bg_sprite_list'):
            self.bg_sprite_list.draw()
        
        # Draw the grid on top of the background
        if hasattr(self, 'show_grid'):
            self.show_grid.draw()
            
    def on_key_press(self, key, modifiers):
        # Press ESC to go back to the main Menu
        if key == arcade.key.ESCAPE:
            from src.frontend.Menu import Menu
            menu_view = Menu()
            self.window.show_view(menu_view)
