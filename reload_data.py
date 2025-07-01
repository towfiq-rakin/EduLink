import sqlite3
import pandas as pd
from src.utils.db_utils import DatabaseManager

def reload_dsa_data(csv_file):
    """
    Reload data from CSV into the DSA table, clearing existing data first.

    Args:
        csv_file (str): Path to the CSV file
    """
    db = DatabaseManager()
    if not db.connect():
        print("Failed to connect to database")
        return False

    try:
        # Clear existing data
        db.cursor.execute("DELETE FROM DSA")
        db.commit()
        print("Cleared existing data from DSA table")

        # Read CSV file
        df = pd.read_csv(csv_file)

        # Check and rename columns if needed
        if 'StudentID' in df.columns:
            df = df.rename(columns={'StudentID': 'student_id', 'Student Name': 'student_name'})
        elif 'Student ID' in df.columns:
            df = df.rename(columns={'Student ID': 'student_id', 'Student Name': 'student_name'})
        else:
            print("CSV file missing required student ID column")
            return False

        if 'student_name' not in df.columns:
            print("CSV file missing required student name column")
            return False

        # Clean column names for SQL (remove spaces and special characters)
        df.columns = [col.strip().lower().replace(' ', '_').replace('-', '_') for col in df.columns]

        # Get existing columns from DSA table
        db.cursor.execute("PRAGMA table_info(DSA)")
        valid_columns = [row[1] for row in db.cursor.fetchall()]

        # Filter DataFrame to only include columns that exist in the table
        df = df[[col for col in df.columns if col in valid_columns]]

        if df.empty:
            print("No valid columns found in CSV file")
            return False

        # Convert DataFrame to list of tuples for insertion
        records = df.to_records(index=False)
        data = [tuple(record) for record in records]

        # Insert the data
        columns = ', '.join([f'"{col}"' for col in df.columns])
        placeholders = ', '.join(['?' for _ in df.columns])

        insert_query = f'INSERT INTO DSA ({columns}) VALUES ({placeholders})'
        print(f"Inserting data with columns: {columns}")

        db.cursor.executemany(insert_query, data)
        db.commit()

        # Get count of inserted records
        db.cursor.execute("SELECT COUNT(*) FROM DSA")
        count = db.cursor.fetchone()[0]
        print(f"Successfully imported {count} records into DSA table")
        return True

    except (sqlite3.Error, Exception) as e:
        print(f"Error reloading data: {e}")
        return False

if __name__ == "__main__":
    csv_path = "data/result.csv"
    print(f"Reloading data from {csv_path}...")
    success = reload_dsa_data(csv_path)
    if success:
        print("Data reload completed successfully")
    else:
        print("Data reload failed")
