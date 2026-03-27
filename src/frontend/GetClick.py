class GetClick:
    def __init__(self, show_grid):
        self.show_grid = show_grid

    def _point_in_polygon(self, x, y, polygon):
        # Ray casting algorithm
        n = len(polygon)
        inside = False
        j = n - 1
        for i in range(n):
            xi, yi = polygon[i]
            xj, yj = polygon[j]
            if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
                inside = not inside
            j = i
        return inside

    def get_cell(self, mouse_x, mouse_y):
        """Returns the clicked cell dict {"col", "row", "polygon"} or None."""
        for cell in self.show_grid.cell_data:
            if self._point_in_polygon(mouse_x, mouse_y, cell["polygon"]):
                return cell
        return None

    def get_col_row(self, mouse_x, mouse_y):
        """Returns (col, row) or (None, None) if no cell was hit."""
        cell = self.get_cell(mouse_x, mouse_y)
        if cell:
            return cell["col"], cell["row"]
        return None, None
