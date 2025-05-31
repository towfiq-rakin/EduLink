import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import os
from ..services import accounts_db
from src.gui.teachers_menu import TeachersMenu

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class LoginWindow:
    def __init__(self, master):
        self.master = master
        master.title("BUP EduLink - Login")
        master.geometry("600x440")
        master.resizable(False, False)

        # Ensure DB and table exist, and sample users are present
        accounts_db.create_table_and_seed()

        doodle_path = os.path.join(os.path.dirname(__file__), "..", "resources", "img", "doodle.png")
        doodle = Image.open(doodle_path)
        doodle = ctk.CTkImage(doodle, size=(600, 440))
        self.pattern_label = ctk.CTkLabel(master=self.master, image=doodle)
        self.pattern_label.pack()

        self.frame = ctk.CTkFrame(master=self.master, width=320, height=320)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.label1 = ctk.CTkLabel(
            master=self.frame,
            text="Log into your account",
            font=('Century Gothic', 20, 'bold'),
        )
        self.label1.place(x=50, y=25)

        # Compute base directory relative to this file
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        user_img_path = os.path.join(base_dir, "resources", "img", "user.png")
        pass_img_path = os.path.join(base_dir, "resources", "img", "pass.png")

        # Use CTkImage for proper scaling and to avoid warnings
        user_img = Image.open(user_img_path)
        user_logo = ctk.CTkImage(user_img, size=(16, 16))
        self.user_icon = ctk.CTkLabel(master=self.frame, image=user_logo, text="")
        self.user_icon.place(x=22, y=90)

        self.username_entry = ctk.CTkEntry(master=self.frame, width=220, placeholder_text="Username")
        self.username_entry.place(x=50, y=90)

        pass_img = Image.open(pass_img_path)
        pass_logo = ctk.CTkImage(pass_img, size=(20, 20))
        self.pass_icon = ctk.CTkLabel(master=self.frame, image=pass_logo, text="")
        self.pass_icon.place(x=20, y=145)
        self.pass_entry = ctk.CTkEntry(master=self.frame, width=220, placeholder_text="Password", show="*")
        self.pass_entry.place(x=50, y=145)

        self.status_label = ctk.CTkLabel(master=self.frame, text="", font=('Century Gothic', 12), text_color="red")
        self.status_label.place(x=50, y=180)

        self.forgot_text = ctk.CTkButton(
            master=self.frame,
            width=120,
            text="Forgot Password?",
            font=('Century Gothic', 12),
            command=lambda: print("Forgot Password clicked"),
            fg_color="transparent",
            hover_color="darkred"
        )
        self.forgot_text.place(x=150, y=180)

        self.login_button = ctk.CTkButton(
            master=self.frame,
            width=220,
            text="Login",
            command=self.login
        )
        self.login_button.place(x=50, y=215)

        self.forget_label = ctk.CTkLabel(master=self.frame, text="Don't have an account? ", font=('Century Gothic', 12))
        self.forget_label.place(x=50, y=260)

        self.register_button = ctk.CTkButton(
            master=self.frame,
            width=70,
            text="Register",
            text_color="skyblue",
            fg_color="transparent",
        )
        self.register_button.place(x=200, y=260)

    def login(self):
        username = self.username_entry.get()
        password = self.pass_entry.get()
        if not username or not password:
            # new pop up Warning window to the user to fill in both fields
            warning_window = ctk.CTkToplevel(self.master)
            warning_window.title("Warning")
            warning_window.geometry("300x100+600+400")
            warning_window.resizable(False, False)
            warning_window.configure(bg_color="darkgray")
            warning_window.lift()  # Bring to front
            warning_window.attributes("-topmost", True)  # Always on top
            warning_label = ctk.CTkLabel(warning_window, text="Please fill in both fields.", text_color="red")
            warning_label.pack(pady=10)
            close_button = ctk.CTkButton(warning_window, text="Close", command=warning_window.destroy)
            close_button.pack(pady=10)
            return
        usertype = accounts_db.validate_login(username, password)
        if usertype:
            # Call the TeachersMenu class if usertype is 'teacher'
            if usertype == 'teacher':
                self.master.destroy()
                root = ctk.CTk()
                app = TeachersMenu(root)
                root.mainloop()
        else:
            warning_window2 = ctk.CTkToplevel(self.master)
            warning_window2.title("Warning")
            warning_window2.geometry("300x100+600+400")
            warning_window2.resizable(False, False)
            warning_window2.configure(bg_color="darkgray")
            warning_window2.lift()  # Bring to front
            warning_window2.attributes("-topmost", True)  # Always on top
            warning_label = ctk.CTkLabel(warning_window2, text="Wrong username or password", text_color="red")
            warning_label.pack(pady=10)
            close_button = ctk.CTkButton(warning_window2, text="Close", command=warning_window2.destroy)
            close_button.pack(pady=10)
            return

if __name__ == "__main__":
    root = ctk.CTk()
    app = LoginWindow(root)
    root.mainloop()
