import random
from src.backend.Case import Case

class GenerateMap:
    def __init__(self, difficulty, firstclickpos):
        self.difficulty = difficulty
        self.firstclickpos = firstclickpos  # [x, y]
        self.length = 10 + 5 * difficulty
        self.bomb_count = (self.length ** 2) // (10 - difficulty)
        self.grid = []
        self._generate_empty_grid()
        self._place_bombs()
        self._calculate_values()
        
        # Initial cascade from first click
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
            if [x, y] not in safe_zone and not self.grid[y][x].isBomb:
                self.grid[y][x].transform()
                bombs_placed += 1

    def _calculate_values(self):
        for y in range(self.length):
            for x in range(self.length):
                if self.grid[y][x].isBomb:
                    self._increment_neighbors(x, y)

    def _increment_neighbors(self, x, y):
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue
                
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.length and 0 <= ny < self.length:
                    self.grid[ny][nx].increaseValue()

    def reveal_cells(self, x, y):
        # Base cases: out of bounds or already revealed
        if not (0 <= x < self.length and 0 <= y < self.length):
            return
        
        case = self.grid[y][x]
        if case.isRevealed:
            return
        
        # Reveal the cell
        case.reveal()
        
        # If the cell is empty (Value == 0 and not a bomb), recurse
        if case.Value == 0 and not case.isBomb:
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if dx == 0 and dy == 0:
                        continue
                    self.reveal_cells(x + dx, y + dy)

    def get_map(self):
        return self.grid