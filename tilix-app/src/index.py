from tkinter import Tk
from src.ui.ui import UI
from src.db import initialize_database

def main():
    initialize_database()
    window = Tk()
    window.title("Tilix")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry(f"{screen_width}x{screen_height}")
    ui_view = UI(window)
    ui_view.start()

    window.mainloop()

if __name__ == "__main__":
    main()
