# Contents of /EduLink/EduLink/src/main.py

import customtkinter as ctk
from src.gui.login import LoginWindow
from src.gui.teachers_menu import TeachersMenu

def main():
    root = ctk.CTk()
    root.title("BUP EduLink")
    app = TeachersMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()
