import arcade
import arcade.gui

class Menu(arcade.View):
    """
    Main menu for the Minesweeper game
    """
    def __init__(self):
        super().__init__()
        
        # 1. Constants and State
        self._init_constants()
        
        # 2. Shader Setup
        self._setup_shader()
        
        # 3. Assets Loading
        self._load_assets()
        
        # 4. User Interface Setup
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self._setup_ui()

    def _init_constants(self):
        """ Initialize level definitions and UI styles """
        self.levels = [("FACILE", 1), ("MOYEN", 2), ("DIFFICILE", 3)]
        self.current_level_index = 1
        
        self.level_style = {
            "normal": {"bg": (60, 60, 60), "font_color": arcade.color.WHITE},
            "hover": {"bg": (60, 60, 60), "font_color": arcade.color.WHITE},
            "press": {"bg": (60, 60, 60), "font_color": arcade.color.WHITE},
        }

    def _setup_shader(self):
        """ Configure the GPU shader for the mouse glow effect """
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
        """ Load all necessary textures for the menu """
        # Load background as an OpenGL texture for the shader
        self.tex_bg = self.window.ctx.load_texture("src/public/img/assets/bg.jpg")
        
        # Load GUI Button Textures
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

    def _setup_ui(self):
        """ Construct the UI layout components """
        self.anchor = arcade.gui.UIAnchorLayout()
        self.v_box = arcade.gui.UIBoxLayout()
        
        # --- PLAY BUTTON ---
        self.play_button = arcade.gui.UITextureButton(
            texture=self.tex_play,
            texture_hovered=self.tex_play_hover,
            texture_pressed=self.tex_play_hover,
            width=250, height=80
        )
        @self.play_button.event("on_click")
        def on_click_play(event):
            level_name, level_id = self.levels[self.current_level_index]
            print(f"Lancement du jeu - Niveau : {level_id} ({level_name})")

        self.v_box.add(self.play_button)
        self.v_box.add(arcade.gui.UISpace(height=40))

        # Central Button (Image + Text Overlay + Arrows Inside)
        self.level_button = arcade.gui.UITextureButton(
            texture=self.tex_lvl,
            width=350, height=100
        )
        @self.level_button.event("on_click")
        def on_click_level(event):
            self.current_level_index = (self.current_level_index + 1) % len(self.levels)
            self.update_level_label()

        self.level_label = arcade.gui.UILabel(
            text=self.levels[self.current_level_index][0],
            font_size=16, font_name="Arial", text_color=arcade.color.WHITE
        )

        # Re-creating arrows to be children of the anchor layout
        left_button = arcade.gui.UITextureButton(
            texture=self.tex_left,
            texture_hovered=self.tex_left_hover,
            texture_pressed=self.tex_left_hover,
            width=30, height=30
        )
        @left_button.event("on_click")
        def on_click_left(event):
            self.current_level_index = (self.current_level_index - 1) % len(self.levels)
            self.update_level_label()

        right_button = arcade.gui.UITextureButton(
            texture=self.tex_right,
            texture_hovered=self.tex_right_hover,
            texture_pressed=self.tex_right_hover,
            width=30, height=30
        )
        @right_button.event("on_click")
        def on_click_right(event):
            self.current_level_index = (self.current_level_index + 1) % len(self.levels)
            self.update_level_label()

        # Layout to group everything (wider than the frame to put arrows outside)
        level_container = arcade.gui.UIAnchorLayout(width=600, height=100)
        level_container.add(self.level_button, anchor_x="center_x", anchor_y="center_y")
        level_container.add(self.level_label, anchor_x="center_x", anchor_y="center_y")
        
        # Placing arrows at the very edges of the 450px layout
        level_container.add(left_button, anchor_x="left", anchor_y="center_y")
        level_container.add(right_button, anchor_x="right", anchor_y="center_y")

        self.v_box.add(level_container)
        self.v_box.add(arcade.gui.UISpace(height=60))

        # --- QUIT BUTTON ---
        self.quit_button = arcade.gui.UITextureButton(
            texture=self.tex_quit,
            texture_hovered=self.tex_quit_hover,
            texture_pressed=self.tex_quit_hover,
            width=250, height=80
        )
        @self.quit_button.event("on_click")
        def on_click_quit(event):
            arcade.exit()

        self.v_box.add(self.quit_button)
        
        self.anchor.add(child=self.v_box, anchor_x="center_x", anchor_y="center_y")
        self.manager.add(self.anchor)

    def update_level_label(self):
        """ Update text on the level selector """
        self.level_label.text = self.levels[self.current_level_index][0]

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.u_mouse = (x, y)

    def on_draw(self):
        """ Unified drawing logic """
        self.clear()
        
        # 1. Update Shader Uniforms
        self.tex_bg.use(0)
        self.shader["u_texture"] = 0
        
        size = self.window.get_framebuffer_size()
        ratio = size[0] / self.window.width
        
        self.shader["u_mouse"] = (self.u_mouse[0] * ratio, self.u_mouse[1] * ratio)
        self.shader["u_resolution"] = size
        
        # 2. Draw Background with Shader
        self.quad.render(self.shader)
        
        # 3. Draw UI Components
        self.manager.draw()

if __name__ == "__main__":
    window = arcade.Window(800, 600, "Minesweeper Menu", resizable=True)
    menu_view = Menu()
    window.show_view(menu_view)
    arcade.run()