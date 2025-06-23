import customtkinter as ctk
from gui.login import LoginWindow
from gui.teachers_menu import TeachersMenu

def main():
    root = ctk.CTk()
    root.title("BUP EduLink")
    app = TeachersMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()