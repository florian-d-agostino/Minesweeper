class Case : 
    def __init__(self):
        self.value = 0
        self.is_bomb = False
        self.is_revealed = False
        self.is_marked = 0

    def transform_case(self):
        self.is_bomb = True

    def reveal_case(self):
        self.is_revealed = True
        
    def toggle_mark(self):
        match self.is_marked:
            case 0:
                self.is_marked = 1
            case 1:
                self.is_marked = 2
            case 2:
                self.is_marked = 0