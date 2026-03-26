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
        self._precompute_grid()
        
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
        
    def draw(self):
        # Draw each pre-calculated polygon
        for cell in self.cell_data:
            polygon = cell["polygon"]
            
            # Draw the filled interior
            arcade.draw_polygon_filled(polygon, self.bg_color)
            
            # Draw the neon outline (making it look like a wireframe grid)
            arcade.draw_polygon_outline(polygon, self.border_color, 2.0)
