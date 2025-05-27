# Contents of /EduLink/EduLink/src/main.py

import tkinter as tk
from gui.main_window import MainWindow

def main():
    root = tk.Tk()
    root.title("EduLink - Student Management App")
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()