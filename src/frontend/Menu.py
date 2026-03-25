import arcade
import arcade.gui

class Menu(arcade.View):
    """
    Main menu for the game
    """
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        
        # ---- CHARGEMENT DU FOND ET SHADER ----
        # On charge l'image directement comme une texture OpenGL pour le shader
        self.tex_bg = self.window.ctx.load_texture("src/public/img/assets/bg.jpg")
        
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
            vec3 light = vec3(0.1, 0.4, 0.7) * pow(glow, 1.2);
            fragColor = vec4(base_color.rgb * vignette + light, 1.0);
        }
        """
        self.u_mouse = (0, 0)
        self.shader = self.window.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        self.quad = arcade.gl.geometry.quad_2d_fs()

        self.anchor = arcade.gui.UIAnchorLayout()
        self.v_box = arcade.gui.UIBoxLayout()
        
        # ---- STYLES DES BOUTONS ----
        self.buttons_style = {
            "normal": {"bg": arcade.color.CYBER_YELLOW, "font_color": arcade.color.BLACK},
            "hover": {"bg": arcade.color.CYBER_GRAPE, "font_color": arcade.color.WHITE},
            "press": {"bg": arcade.color.DARK_BLUE, "font_color": arcade.color.WHITE},
        }
        self.quit_style = {
            "normal": {"bg": arcade.color.CYBER_YELLOW, "font_color": arcade.color.BLACK},
            "hover": {"bg": arcade.color.CYBER_GRAPE, "font_color": arcade.color.WHITE},
            "press": {"bg": arcade.color.CYBER_GRAPE, "font_color": arcade.color.WHITE},
        }
        self.level_style = {
            "normal": {"bg": (60, 60, 60), "font_color": arcade.color.WHITE},
            "hover": {"bg": (60, 60, 60), "font_color": arcade.color.WHITE},
            "press": {"bg": (60, 60, 60), "font_color": arcade.color.WHITE},
        }

        # ---- CHARGEMENT DES TEXTURES PERSONNALISÉES ----
        self.tex_play = arcade.load_texture("src/public/img/assets/play.png")
        self.tex_play_hover = arcade.load_texture("src/public/img/assets/play_hover.png")
        self.tex_quit = arcade.load_texture("src/public/img/assets/quitter.png")
        self.tex_quit_hover = arcade.load_texture("src/public/img/assets/quitter_hover.png")
        self.tex_left = arcade.load_texture("src/public/img/assets/arrow_left.png")
        self.tex_left_hover = arcade.load_texture("src/public/img/assets/arrow_left_hover.png")
        self.tex_right = arcade.load_texture("src/public/img/assets/arrow_right.png")
        self.tex_right_hover = arcade.load_texture("src/public/img/assets/arrow_right_hover.png")

        # Bouton JOUER
        self.play_button = arcade.gui.UITextureButton(
            texture=self.tex_play,
            texture_hovered=self.tex_play_hover,
            texture_pressed=self.tex_play_hover,
            width=250,
            height=80
        )
        self.v_box.add(self.play_button)
        self.v_box.add(arcade.gui.UISpace(height=40))

        # ---- SÉLECTEUR DE DIFFICULTÉ ----
        self.levels = [("FACILE", 0), ("INTERMÉDIAIRE", 1), ("EXPERT", 2)]
        self.current_level_index = 1
        self.h_box = arcade.gui.UIBoxLayout(vertical=False)

        left_button = arcade.gui.UITextureButton(
            texture=self.tex_left,
            texture_hovered=self.tex_left_hover,
            texture_pressed=self.tex_left_hover,
            width=50,
            height=50
        )
        @left_button.event("on_click")
        def on_click_left(event):
            self.current_level_index = (self.current_level_index - 1) % len(self.levels)
            self.update_level_label()

        right_button = arcade.gui.UITextureButton(
            texture=self.tex_right,
            texture_hovered=self.tex_right_hover,
            texture_pressed=self.tex_right_hover,
            width=50,
            height=50
        )
        @right_button.event("on_click")
        def on_click_right(event):
            self.current_level_index = (self.current_level_index + 1) % len(self.levels)
            self.update_level_label()

        # Difficulty Selector
        self.level_display = arcade.gui.UIFlatButton(
            text=self.levels[self.current_level_index][0],
            width=170,
            style=self.level_style
        )

        self.h_box.add(left_button)
        self.h_box.add(self.level_display)
        self.h_box.add(right_button)
        self.v_box.add(self.h_box)

        # Quit Button
        self.v_box.add(arcade.gui.UISpace(height=20))
        self.quit_button = arcade.gui.UITextureButton(
            texture=self.tex_quit,
            texture_hovered=self.tex_quit_hover,
            texture_pressed=self.tex_quit_hover,
            width=250,
            height=80
        )
        self.v_box.add(self.quit_button)
        @self.quit_button.event("on_click")
        def on_click_quit(event):
            arcade.exit()

        # Play Button
        @self.play_button.event("on_click")
        def on_click_play(event):
            level_name, level_id = self.levels[self.current_level_index]
            print(f"Lancement du jeu - Niveau : {level_id} ({level_name})")

        self.anchor.add(child=self.v_box, anchor_x="center_x", anchor_y="center_y")
        self.manager.add(self.anchor)

    def update_level_label(self):
        self.level_display.text = self.levels[self.current_level_index][0]

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.u_mouse = (x, y)


    # Draw
    def on_draw(self):
        self.clear()
        
        # Configuration de la texture pour le shader
        self.tex_bg.use(0)
        self.shader["u_texture"] = 0
        
        pixel_width, pixel_height = self.window.get_framebuffer_size()
        window_width, window_height = self.window.get_size()
        ratio = pixel_width / window_width
        
        # Envoi des variables au GPU
        self.shader["u_mouse"] = (self.u_mouse[0] * ratio, self.u_mouse[1] * ratio)
        self.shader["u_resolution"] = (pixel_width, pixel_height)
        
        # Rendu du fond via le shader
        self.quad.render(self.shader)
        
        self.manager.draw()

if __name__ == "__main__":
    window = arcade.Window(800, 600, "Minesweeper Menu", resizable=True)
    menu_view = Menu()
    window.show_view(menu_view)
    arcade.run()