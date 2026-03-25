class Case:
    def __init__(self, pos):
        self.pos = pos  # [x, y]
        self.isBomb = False
        self.isRevealed = False
        self.Value = 0

    def transform(self):
        self.isBomb = True

    def increaseValue(self):
        self.Value += 1

    def reveal(self):
        self.isRevealed = True
