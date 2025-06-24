import os
import sys
import pandas as pd
from pathlib import Path

# Add the project root to the Python path for imports
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_dir)

from src.utils.db_utils import DatabaseManager
from src.utils.import_grades import import_grades_to_db

def initialize_database():
    """
    Initialize the student database by creating the necessary tables
    and importing data from CSV files.

    Returns:
        bool: True if initialization was successful, False otherwise
    """
    # Initialize the database manager
    db_manager = DatabaseManager()

    # Get paths to data files
    data_dir = os.path.join(root_dir, 'data')
    result_csv = os.path.join(data_dir, 'result.csv')

    # Connect to the database
    if not db_manager.connect():
        print("Failed to connect to the database.")
        return False

    try:
        # Create tables
        print("Creating database tables...")
        if not db_manager.create_tables():
            print("Failed to create tables.")
            return False

        # Import result data
        print(f"Importing data from {result_csv}...")
        success, count = db_manager.import_result_data(result_csv)
        if not success:
            print("Failed to import result data.")
            return False
        print(f"Successfully imported {count} student records.")

        # Import grade data
        print("Setting up grade information...")
        if not db_manager.import_grade_data():
            print("Failed to import grade data.")
            return False
        print("Grade information successfully set up.")
        # Import student grades and allocate scholarships
        print("Importing student grades and processing scholarships...")
        import_grades_to_db()

        print("Database initialization completed successfully!")
        return True

    except Exception as e:
        print(f"Error during database initialization: {e}")
        return False

    finally:
        # Always disconnect from the database
        db_manager.disconnect()

def get_db_stats():
    """
    Get statistics about the database.

    Returns:
        dict: Dictionary containing database statistics
    """
    db_manager = DatabaseManager()
    if not db_manager.connect():
        print("Failed to connect to the database.")
        return {}

    try:
        # Get statistics
        stats = db_manager.get_statistics()

        # Check if the database file exists and get its size
        db_path = db_manager.db_path
        if os.path.exists(db_path):
            stats['db_file_size'] = os.path.getsize(db_path) / (1024 * 1024)  # Size in MB
            stats['db_file_path'] = db_path

        return stats

    except Exception as e:
        print(f"Error getting database statistics: {e}")
        return {}

    finally:
        db_manager.disconnect()

if __name__ == "__main__":
    # If this script is run directly, initialize the database
    initialize_database()

    # Print some statistics
    print("\nDatabase Statistics:")
    stats = get_db_stats()
    if stats:
        print(f"Total students: {stats.get('total_students', 0)}")
        print(f"Average percentage: {stats.get('average_percentage', 0):.2f}%")
        print(f"Database file size: {stats.get('db_file_size', 0):.2f} MB")
        print(f"Database location: {stats.get('db_file_path', 'Unknown')}")

        print("\nGrade Distribution:")
        for grade, count in stats.get('grade_distribution', {}).items():
            print(f"  {grade}: {count} students")
    else:
        print("No statistics available.")
