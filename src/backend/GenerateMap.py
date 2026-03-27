import random
from src.backend.Case import Case

class GenerateMap:
    # Grid sizes must match ShowGrid
    GRID_SIZES = {1: 9, 2: 11, 3: 13}
    BOMB_COUNTS = {1: 10, 2: 15, 3: 25}

    def __init__(self, level_id, firstclickpos):
        self.level_id = level_id
        self.firstclickpos = firstclickpos  # [col, row]
        self.length = self.GRID_SIZES.get(level_id, 9)
        self.bomb_count = self.BOMB_COUNTS.get(level_id, 10)
        self.grid = []
        self._generate_empty_grid()
        self._place_bombs()
        self._calculate_values()
        self.reveal_cells(self.firstclickpos[0], self.firstclickpos[1])

    def _generate_empty_grid(self):
        for y in range(self.length):
            row = []
            for x in range(self.length):
                row.append(Case([x, y]))
            self.grid.append(row)

    def _place_bombs(self):
        bombs_placed = 0
        safe_zone = []
        # Calculate 3x3 safe zone around first click
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                nx, ny = self.firstclickpos[0] + dx, self.firstclickpos[1] + dy
                if 0 <= nx < self.length and 0 <= ny < self.length:
                    safe_zone.append([nx, ny])

        while bombs_placed < self.bomb_count:
            x = random.randint(0, self.length - 1)
            y = random.randint(0, self.length - 1)
            
            # Avoid placing bomb in the safe zone and avoid duplicates
            if [x, y] not in safe_zone and not self.grid[y][x].is_bomb:
                self.grid[y][x].transform_case()
                bombs_placed += 1

    def _calculate_values(self):
        for y in range(self.length):
            for x in range(self.length):
                if self.grid[y][x].is_bomb:
                    self._increment_neighbors(x, y)

    def _increment_neighbors(self, x, y):
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue
                
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.length and 0 <= ny < self.length:
                    self.grid[ny][nx].increase_value()

    def reveal_cells(self, x, y):
        # Base cases: out of bounds or already revealed
        if not (0 <= x < self.length and 0 <= y < self.length):
            return False
        
        case = self.grid[y][x]
        if case.is_revealed or case.is_marked > 0:
            return False
        
        case.reveal_case()
        
        if case.is_bomb:
            return True
        
        if case.value == 0:
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if dx == 0 and dy == 0:
                        continue
                    self.reveal_cells(x + dx, y + dy)
        
        return False

    def get_map(self):
        return self.grid

    def check_victory(self):
        for y in range(self.length):
            for x in range(self.length):
                case = self.grid[y][x]
                if not case.is_bomb and not case.is_revealed:
                    return False
        return True

    def reveal_all_bombs(self):
        for row in self.grid:
            for case in row:
                if case.is_bomb:
                    case.is_revealed = True