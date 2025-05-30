# Contents of /EduLink/EduLink/src/main.py

import customtkinter as ctk
from src.gui.login import LoginWindow

def main():
    root = ctk.CTk()
    root.title("BUP EduLink")
    app = LoginWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
