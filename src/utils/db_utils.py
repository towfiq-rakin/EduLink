import os
import sqlite3
import pandas as pd
import csv

class DatabaseManager:
    """
    A utility class to manage SQLite database operations for the EduLink application.
    Handles creating tables, importing data from CSV files, and querying the database.
    """

    def __init__(self, db_path=None):
        """
        Initialize the database manager with a path to the database file.

        Args:
            db_path (str): Path to the SQLite database file. If None, creates a default path.
        """
        if db_path is None:
            # Create database in the data directory
            base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            db_path = os.path.join(base_path, 'data', 'student.db')

        self.db_path = db_path
        self.connection = None
        self.cursor = None

    def connect(self):
        """
        Establish a connection to the SQLite database.

        Returns:
            bool: True if connection was successful, False otherwise.
        """
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            return True
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            return False

    def disconnect(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None

    def execute_query(self, query, params=None):
        """
        Execute a SQL query.

        Args:
            query (str): SQL query to execute
            params (tuple, optional): Parameters for the query

        Returns:
            The cursor object or None if there's an error
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor
        except sqlite3.Error as e:
            print(f"Query execution error: {e}")
            print(f"Query: {query}")
            return None

    def commit(self):
        """Commit changes to the database."""
        self.connection.commit()

    def create_tables(self):
        """
        Create the necessary tables in the database if they don't exist.

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create DSA table for storing result.csv data
            self.execute_query('''
            CREATE TABLE IF NOT EXISTS DSA (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                student_name TEXT NOT NULL,
                CT1 REAL,
                CT2 REAL,
                CT3 REAL,
                CT4 REAL,
                mid_term REAL,
                presentation REAL,
                attendance REAL,
                best_3_CT_avg REAL,
                midterm_scaled REAL,
                total_obtained REAL,
                percentage REAL,
                grade TEXT,
                UNIQUE(student_id)
            )''')

            self.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")
            return False

    def import_result_data(self, csv_file):
        """
        Import data from result.csv into the DSA table.

        Args:
            csv_file (str): Path to the CSV file

        Returns:
            tuple: (success: bool, count: int)
        """
        try:
            # First check if we have data in the DSA table
            self.cursor.execute("SELECT COUNT(*) FROM DSA")
            count = self.cursor.fetchone()[0]

            if count > 0:
                print("DSA table already contains data. Skipping import.")
                return True, count

            # Read CSV file
            df = pd.read_csv(csv_file)

            # Check for required columns with both possible naming conventions
            if 'StudentID' in df.columns:
                df = df.rename(columns={'StudentID': 'student_id', 'Student Name': 'student_name'})
            elif 'Student ID' in df.columns:
                df = df.rename(columns={'Student ID': 'student_id', 'Student Name': 'student_name'})
            else:
                print("CSV file missing required student ID column")
                return False, 0

            if 'student_name' not in df.columns:
                print("CSV file missing required student name column")
                return False, 0

            # Convert student_id to integer and handle any invalid values
            df['student_id'] = pd.to_numeric(df['student_id'], errors='coerce')
            df = df.dropna(subset=['student_id'])
            df['student_id'] = df['student_id'].astype(int)

            # Prepare data for insertion
            for _, row in df.iterrows():
                try:
                    self.cursor.execute('''
                    INSERT INTO DSA (
                        student_id, student_name, CT1, CT2, CT3, CT4,
                        mid_term, presentation, attendance
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        int(row['student_id']),
                        row['student_name'],
                        row.get('CT1', 0),
                        row.get('CT2', 0),
                        row.get('CT3', 0),
                        row.get('CT4', 0),
                        row.get('Mid-Term', 0),
                        row.get('Presentation', 0),
                        row.get('Attendance', 8)  # Default attendance value
                    ))
                except sqlite3.IntegrityError:
                    # Skip duplicate student_id
                    continue

            self.commit()

            # Get final count of inserted records
            self.cursor.execute("SELECT COUNT(*) FROM DSA")
            final_count = self.cursor.fetchone()[0]

            return True, final_count

        except Exception as e:
            print(f"Error importing result data: {e}")
            return False, 0

    def import_grade_data(self):
        """Set up grade information in the database"""
        try:
            # Nothing to import for now, just return True
            return True
        except Exception as e:
            print(f"Error importing grade data: {e}")
            return False

    def get_statistics(self):
        """Get database statistics"""
        try:
            stats = {}
            self.cursor.execute("SELECT COUNT(*) FROM DSA")
            stats['total_students'] = self.cursor.fetchone()[0]
            return stats
        except sqlite3.Error as e:
            print(f"Error getting statistics: {e}")
            return {}

    def get_all_students(self):
        """
        Get all student records from the DSA table.

        Returns:
            pd.DataFrame: DataFrame containing all student records, or None if error
        """
        try:
            # Create the SQL query
            query = """
            SELECT student_id, student_name, CT1, CT2, CT3, CT4,
                   mid_term, presentation, attendance,
                   best_3_ct_avg, midterm_scaled, total_obtained,
                   percentage, grade
            FROM DSA
            ORDER BY student_id
            """

            # Execute the query and fetch all records
            df = pd.read_sql_query(query, self.connection)

            # Rename columns to match the expected format
            column_mapping = {
                'student_id': 'Student ID',
                'student_name': 'Student Name',
                'mid_term': 'Mid-Term',
                'presentation': 'Presentation',
                'attendance': 'Attendance',
                'total_obtained': 'Total_Obtained',
                'percentage': 'Percentage'
            }
            df = df.rename(columns=column_mapping)

            return df

        except Exception as e:
            print(f"Error getting student records: {e}")
            return None

