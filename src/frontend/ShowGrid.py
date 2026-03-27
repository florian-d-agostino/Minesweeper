import arcade

class ShowGrid:
    def __init__(self, level_id, screen_width, screen_height):
        # Map level_id to grid size
        if level_id == 1:
            self.cols, self.rows = 9, 9
        elif level_id == 2:
            self.cols, self.rows = 11, 11
        elif level_id == 3:
            self.cols, self.rows = 13, 13
        else:
            self.cols, self.rows = 9, 9
            
        # Cell size per difficulty level (cell_width, cell_height)
        cell_sizes = {
            1: (46, 41),     # Easy       — edit here
            2: (37, 33.5),   # Medium     — kept as reference
            3: (31, 27.5),   # Hard       — edit here
        }
        self.cell_width, self.cell_height = cell_sizes.get(level_id, (37, 33.5))
        self.cell_margin = 3
        
        self.grid_width  = self.cell_width  * self.cols + self.cell_margin * (self.cols - 1)
        self.grid_height = self.cell_height * self.rows + self.cell_margin * (self.rows - 1) - 28
        
        self.center_x = screen_width / 2
        
        # Center the grid, shifted slightly down to align with the background image grid
        self.start_y = (screen_height - self.grid_height) / 2 - 40
        self.start_x = self.center_x - self.grid_width / 2
        
        # Colors (Cyberpunk theme)
        self.bg_color = (20, 30, 50, 200)       # Dark translucent blue for inside
        self.border_color = (0, 255, 255, 180)  # Neon cyan for borders
        
        self.cell_data = []
        self.text_objects = {}  # Cache for arcade.Text objects
        self._precompute_grid()
        self.bomb_texture = arcade.load_texture("src/public/img/assets/bomb.png")
        
    def _precompute_grid(self):
        """ Calculate the perspective polygons for every cell once so it is fast to draw. """
        self.cell_data.clear()
        
        for row in range(self.rows):
            for col in range(self.cols):
                # Calculate flat 2D bounds for the current cell
                left   = self.start_x + col * (self.cell_width  + self.cell_margin)
                right  = left + self.cell_width
                bottom = self.start_y + row * (self.cell_height + self.cell_margin)
                top    = bottom + self.cell_height
                
                # Transform to pseudo-3D perspective points
                p1 = self.project_point(left, bottom)
                p2 = self.project_point(right, bottom)
                p3 = self.project_point(right, top)
                p4 = self.project_point(left, top)
                
                polygon = [p1, p2, p3, p4]
                
                self.cell_data.append({
                    "col": col, 
                    "row": row, 
                    "polygon": polygon
                })
                
                # Pre-create text objects for values 1-8 at this position
                cx = sum(p[0] for p in polygon) / 4
                cy = sum(p[1] for p in polygon) / 4
                
                # Classic readable colors per value
                value_colors = {
                    1: (30, 80, 200),   # deep blue
                    2: (30, 140, 60),   # forest green
                    3: (200, 40, 40),   # dark red
                    4: (90, 20, 140),   # purple
                    5: (170, 50, 20),   # brown
                    6: (20, 140, 140),  # teal
                    7: (30, 30, 30),    # near black
                    8: (90, 90, 90),    # grey
                }
                
                for val in range(1, 9):
                    color = value_colors.get(val, (0, 0, 0))
                    self.text_objects[(col, row, val)] = arcade.Text(
                        str(val), cx, cy, color,
                        font_size=10, font_name="Orbitron",
                        anchor_x="center", anchor_y="center", bold=True
                    )

    def project_point(self, x, y):
        """ Applies a trapezoidal perspective projection so the grid looks like a 3D floor """
        dy = y - self.start_y
        progress = dy / self.grid_height
        
        # Foreshortening: Compress the distance as it goes further away (Y-axis)
        perspective_y = self.start_y + self.grid_height * (progress ** 0.9)
        
        # Horizontal Vanishing Point Squeeze (Trapezoid effect)
        squeeze = 1.0 - (progress * 0.17)
        
        perspective_x = self.center_x + (x - self.center_x) * squeeze
        
        return perspective_x, perspective_y
        
    def draw(self, grid=None):
        # Colors for each cell state
        color_hidden   = (20, 30, 50, 200)
        color_revealed = (240, 200, 80, 240)
        color_bomb     = (200, 30, 30, 230)
        color_flagged  = (200, 130, 0, 230)
        border_color   = (0, 255, 255, 180)

        # Classic readable colors per value
        value_colors = {
            1: (30, 80, 200),   # deep blue
            2: (30, 140, 60),   # forest green
            3: (200, 40, 40),   # dark red
            4: (90, 20, 140),   # purple
            5: (170, 50, 20),   # brown
            6: (20, 140, 140),  # teal
            7: (30, 30, 30),    # near black
            8: (90, 90, 90),    # grey
        }

        for cell in self.cell_data:
            polygon = cell["polygon"]
            col, row = cell["col"], cell["row"]

            # Determine fill color from game state
            fill = color_hidden
            case = None
            if grid is not None:
                case = grid[row][col]
                if case.is_marked > 0:
                    fill = color_flagged
                elif case.is_revealed:
                    fill = color_bomb if case.is_bomb else color_revealed

            arcade.draw_polygon_filled(polygon, fill)
            arcade.draw_polygon_outline(polygon, border_color, 2.0)

            if case and case.is_revealed and case.is_bomb:
                cx = sum(p[0] for p in polygon) / 4
                cy = sum(p[1] for p in polygon) / 4
                size = min(self.cell_width, self.cell_height) * 0.8
                arcade.draw_texture_rect(
                    self.bomb_texture,
                    arcade.LBWH(cx - size / 2, cy - size / 2, size, size)
                )

            elif case and case.is_revealed and not case.is_bomb and 0 < case.value < 9:
                # Use pre-created text object
                self.text_objects[(col, row, case.value)].draw()

