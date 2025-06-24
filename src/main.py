import customtkinter as ctk
import os
import sys

# Add project root to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(project_root)

from gui.login import LoginWindow
from gui.teachers_menu import TeachersMenu
from src.utils.initialize_db import initialize_database, get_db_stats

def main():
    # Initialize SQLite database
    print("Initializing student database...")
    db_initialized = initialize_database()

    if db_initialized:
        print("Database initialized successfully!")
        stats = get_db_stats()
        if stats:
            print(f"Database contains {stats.get('total_students', 0)} student records")
    else:
        print("Database initialization failed, will proceed with CSV-based data.")

    # Start the application
    root = ctk.CTk()
    root.title("BUP EduLink")
    app = TeachersMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()