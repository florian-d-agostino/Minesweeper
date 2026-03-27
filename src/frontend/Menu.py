import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import arcade
import arcade.gui
import random
import json
from pathlib import Path

class Menu(arcade.View):
    """
    Main menu for the Minesweeper game featuring a Cyberpunk aesthetic with:
    - GPU-powered mouse glow shader
    - Texture-based buttons and frames
    - Foundational sound and music integration
    - Faulty neon "glitch" animations on hover
    """
    def __init__(self):
        super().__init__()
        
        # 1. Constants
        self._init_constants()
        self.pulse_timer = 0.0
        self.next_glitch_time = random.uniform(2, 5)
        self.glitch_end_time = 0.0
        
        # 2. Shader
        self._setup_shader()
        
        # 3. Asset Management 
        self._load_assets()
        
        # 4. User Interface
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self._setup_ui()

    def _init_constants(self):
        """ Difficulty definitions and score load """
        self.levels = [("EASY", 1), ("MEDIUM", 2), ("HARD", 3)]
        self.current_level_index = 1
        
        # Load scores from JSON
        self.score_data = {}
        self._load_scores()

    def _load_scores(self):
        """ Read the high scores from the external JSON file """
        path = Path("src/backend/score.json")
        try:
            if path.exists():
                with open(path, "r") as f:
                    self.score_data = json.load(f)
            else:
                # Default values if file missing
                self.score_data = {"0": "00:00", "1": "00:00", "2": "00:00"}
        except Exception as e:
            print(f"Error loading scores: {e}")
            self.score_data = {"0": "00:00", "1": "00:00", "2": "00:00"}

    def _setup_shader(self):
        """ Initialize the CRT-style mouse glow shader """
        vertex_shader = """
        #version 330
        in vec2 in_vert;
        void main() {
            gl_Position = vec4(in_vert, 0.0, 1.0);
        }
        """
        fragment_shader = """
        #version 330
        uniform vec2 u_mouse;
        uniform vec2 u_resolution;
        uniform sampler2D u_texture;
        out vec4 fragColor;
        void main() {
            vec2 uv = gl_FragCoord.xy / u_resolution;
            vec4 base_color = texture(u_texture, uv);
            float dist = distance(gl_FragCoord.xy, u_mouse);
            float glow = 1.0 / (dist * 0.01 + 1.0);
            float vignette = distance(uv, vec2(0.5, 0.5));
            vignette = 1.0 - smoothstep(0.4, 1.2, vignette);
            vec3 light = vec3(1.0, 0.8, 0.0) * pow(glow, 1.2);
            fragColor = vec4(base_color.rgb * vignette + light, 1.0);
        }
        """
        self.u_mouse = (0, 0)
        self.shader = self.window.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        self.quad = arcade.gl.geometry.quad_2d_fs()

    def _load_assets(self):
        """ Load all images, fonts, and sounds once at startup """
        # Background Texture (native GL load for shader support)
        self.tex_bg = self.window.ctx.load_texture("src/public/img/assets/bg.jpg")
        
        # GUI Textures
        path = "src/public/img/assets"
        self.tex_play = arcade.load_texture(f"{path}/play.png")
        self.tex_play_hover = arcade.load_texture(f"{path}/play_hover.png")
        self.tex_quit = arcade.load_texture(f"{path}/quitter.png")
        self.tex_quit_hover = arcade.load_texture(f"{path}/quitter_hover.png")
        self.tex_left = arcade.load_texture(f"{path}/arrow_left.png")
        self.tex_left_hover = arcade.load_texture(f"{path}/arrow_left_hover.png")
        self.tex_right = arcade.load_texture(f"{path}/arrow_right.png")
        self.tex_right_hover = arcade.load_texture(f"{path}/arrow_right_hover.png")
        self.tex_lvl = arcade.load_texture(f"{path}/lvl.png")
        self.tex_score = arcade.load_texture(f"{path}/score.png")
        
        # Font Assets
        arcade.load_font("src/public/assets/Orbitron-Bold.ttf")
        
        # Sound Assets
        self.music = arcade.load_sound("src/public/assets/Chrome Halo.mp3")
        self.music_player = self.music.play(loop=True, volume=0.5)

    def _setup_ui(self):
        """ Build the responsive layout with UIManager """
        self.anchor = arcade.gui.UIAnchorLayout()
        self.v_box = arcade.gui.UIBoxLayout(space_between=20)







        # --- PLAY BUTTON ---
        self.play_button = arcade.gui.UITextureButton(
            texture=self.tex_play,
            texture_hovered=self.tex_play_hover,
            texture_pressed=self.tex_play_hover,
            width=250, height=80)
        def on_click_play(event):
            level_name, level_id = self.levels[self.current_level_index]
            print(f"Starting game - Level: {level_id} ({level_name})")
            from src.frontend.SetGame import SetGameView
            game_view = SetGameView(level_id)
            self.window.show_view(game_view)
        self.play_button.on_click = on_click_play
        self.play_button.original_hover_tex = self.play_button.texture_hovered
        self.v_box.add(self.play_button)







        # --- DIFFICULTY SELECTOR ---
        self.level_button = arcade.gui.UITextureButton(
            texture=self.tex_lvl,
            width=350, height=100)
        def on_click_level(event):
            self.current_level_index = (self.current_level_index + 1) % len(self.levels)
            self.update_level_label()
        self.level_button.on_click = on_click_level
        self.level_button.original_hover_tex = self.level_button.texture_hovered
        self.level_label = arcade.gui.UILabel(
            text=self.levels[self.current_level_index][0],
            font_size=20, font_name="Orbitron", text_color=arcade.color.WHITE)



        self.left_button = arcade.gui.UITextureButton(
            texture=self.tex_left,
            texture_hovered=self.tex_left_hover,
            texture_pressed=self.tex_left_hover,
            width=30, height=30)
        def on_click_left(event):
            self.current_level_index = (self.current_level_index - 1) % len(self.levels)
            self.update_level_label()
        self.left_button.on_click = on_click_left
        self.left_button.original_hover_tex = self.left_button.texture_hovered



        self.right_button = arcade.gui.UITextureButton(
            texture=self.tex_right,
            texture_hovered=self.tex_right_hover,
            texture_pressed=self.tex_right_hover,
            width=30, height=30)
        def on_click_right(event):
            self.current_level_index = (self.current_level_index + 1) % len(self.levels)
            self.update_level_label()
        self.right_button.on_click = on_click_right
        self.right_button.original_hover_tex = self.right_button.texture_hovered


        # Anchor difficulty
        level_container = arcade.gui.UIAnchorLayout(
            width=250, height=100, 
            size_hint=(None, None))
        level_container.add(self.level_button, anchor_x="center_x", anchor_y="center_y")
        level_container.add(self.level_label, anchor_x="center_x", anchor_y="center_y")
        level_container.add(self.left_button, anchor_x="left", anchor_y="center_y")
        level_container.add(self.right_button, anchor_x="right", anchor_y="center_y")
        self.v_box.add(level_container)







        # --- QUIT BUTTON ---
        self.quit_button = arcade.gui.UITextureButton(
            texture=self.tex_quit,
            texture_hovered=self.tex_quit_hover,
            texture_pressed=self.tex_quit_hover,
            width=250, height=80)
        def on_click_quit(event):
            arcade.exit()
        self.quit_button.on_click = on_click_quit
        self.quit_button.original_hover_tex = self.quit_button.texture_hovered
        self.v_box.add(self.quit_button)




        # SCORE PANEL 
        self.score_container = arcade.gui.UIAnchorLayout(width=420, height=220, size_hint=(None, None))
        self.score_button = arcade.gui.UITextureButton(
            texture=self.tex_score,
            width=420, height=220)
        self.score_button.alpha = 180
        self.score_button.original_hover_tex = self.score_button.texture_hovered
        self.score_container.add(self.score_button, anchor_x="center_x", anchor_y="center_y")
        self.score_vbox = arcade.gui.UIBoxLayout(space_between=5) 



        # Header
        self.score_vbox.add(arcade.gui.UILabel(
            text="BEST SCORE", 
            font_size=16, font_name="Orbitron", 
            text_color=(255, 255, 0, 230)))


        self.score_entries = []
        for i in range(1, 2): 
            lbl = arcade.gui.UILabel(
                text="", 
                font_size=16, font_name="Orbitron", 
                text_color=(255, 255, 255, 230))
            self.score_vbox.add(lbl)
            self.score_entries.append(lbl)


        # Anchor score
        self.score_container.add(self.score_vbox, anchor_x="center_x", anchor_y="center_y", align_y=10)
        self.update_scores()
        self.anchor.add(child=self.v_box, anchor_x="center_x", anchor_y="center_y", align_y=-50)
        self.anchor.add(child=self.score_container, anchor_x="right", anchor_y="bottom", align_x=25, align_y=-50)
        self.manager.add(self.anchor)

    def update_level_label(self):
        """ Update text on the current level and scoreboard """
        self.level_label.text = self.levels[self.current_level_index][0]
        self.update_scores()

    def update_scores(self):
        """ Refresh the scoreboard based on the current level from score.json """
        time = self.score_data.get(str(self.current_level_index), "00:00")
        if len(self.score_entries) > 0:
            self.score_entries[0].text = f"{time}"

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.u_mouse = (x, y)

    def on_update(self, delta_time):
        """ Global animation timer update """
        self.pulse_timer += delta_time

    def on_draw(self):
        """ Main rendering pipeline """
        self.clear()

        self.tex_bg.use(0)
        self.shader["u_texture"] = 0

        framebuffer_size = self.window.get_framebuffer_size()
        ratio = framebuffer_size[0] / self.window.width
        
        self.shader["u_mouse"] = (self.u_mouse[0] * ratio, self.u_mouse[1] * ratio)
        self.shader["u_resolution"] = framebuffer_size

        self.quad.render(self.shader)
        if self.pulse_timer > self.next_glitch_time:
            self.glitch_end_time = self.pulse_timer + random.uniform(0.3, 0.6)
            self.next_glitch_time = self.glitch_end_time + random.uniform(2, 8)
        is_glitching = self.pulse_timer < self.glitch_end_time
        # Apply flicker to hovered buttons
        all_buttons = [
            self.play_button, self.quit_button, 
            self.level_button, self.left_button, self.right_button,
            self.score_button
        ]

        for btn in all_buttons:
            # Enforce visibility
            btn.visible = True
            
            # Flicker logic using texture swap
            if btn.hovered and is_glitching:
                if random.random() > 0.4:  # Flicker OFF (show non-glow image)
                    btn.texture_hovered = btn.texture
                    # For labels, maybe dim the text?
                    if btn == self.level_button:
                        self.level_label.text_color = (255, 255, 255, 100)
                else:
                    btn.texture_hovered = btn.original_hover_tex
                    if btn == self.level_button:
                        self.level_label.text_color = arcade.color.WHITE
            else:
                # Restore original neon textures
                if hasattr(btn, 'original_hover_tex'):
                    btn.texture_hovered = btn.original_hover_tex
                if btn == self.level_button:
                    self.level_label.text_color = arcade.color.WHITE
        self.manager.draw()

if __name__ == "__main__":
    window = arcade.Window(1024, 569, "Minesweeper Menu", resizable=True)
    menu_view = Menu()
    window.show_view(menu_view)
    arcade.run()