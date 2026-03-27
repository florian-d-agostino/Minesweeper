import arcade

class SetMarker:
    def __init__(self, show_grid, get_click):
        self.show_grid = show_grid
        self.get_click = get_click
        self.marker1 = arcade.load_texture("src/public/img/assets/marker1.png")
        self.marker2 = arcade.load_texture("src/public/img/assets/marker2.png")

    def handle_right_click(self, mouse_x, mouse_y, grid):
        """Toggle the mark on the clicked cell (0 → 1 → 2 → 0)."""
        col, row = self.get_click.get_col_row(mouse_x, mouse_y)
        if col is None or grid is None:
            return
        case = grid[row][col]
        if not case.is_revealed:
            case.toggle_mark()

    def draw_markers(self, grid, cell_data, cell_width, cell_height):
        """Draw marker icons over flagged cells."""
        if grid is None:
            return
        size = min(cell_width, cell_height) * 0.8
        for cell in cell_data:
            case = grid[cell["row"]][cell["col"]]
            if case.is_marked == 0:
                continue
            polygon = cell["polygon"]
            cx = sum(p[0] for p in polygon) / 4
            cy = sum(p[1] for p in polygon) / 4
            texture = self.marker1 if case.is_marked == 1 else self.marker2
            arcade.draw_texture_rect(
                texture,
                arcade.LBWH(cx - size / 2, cy - size / 2, size, size)
            )
