import os
import sys
import sqlite3

# Add the project root to the Python path for imports
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_dir)

def reset_database():
    """Reset the database by removing it and recreating it"""
    try:
        # Get database path
        db_path = os.path.join(root_dir, 'data', 'student.db')

        # Remove existing database if it exists
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f"Removed existing database: {db_path}")

        # Import and run database initialization
        from src.utils.initialize_db import initialize_database
        success = initialize_database()

        if success:
            print("Database has been successfully reset and reinitialized!")
            return True
        else:
            print("Failed to reinitialize database.")
            return False

    except Exception as e:
        print(f"Error during database reset: {e}")
        return False

if __name__ == "__main__":
    reset_database()
