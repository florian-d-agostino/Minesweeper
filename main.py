import arcade
from src.frontend.Menu import Menu

def main():
    """
    Main entry point for the Minesweeper game.
    Initializes the window and shows the main menu.
    """
    window = arcade.Window(1024, 569, "Minesweeper", resizable=True)
    menu_view = Menu()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()