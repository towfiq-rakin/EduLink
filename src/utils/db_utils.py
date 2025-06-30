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
                student_id TEXT,
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
                category TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')

            # Create grade table for storing grade information
            self.execute_query('''
            CREATE TABLE IF NOT EXISTS grade (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                grade TEXT NOT NULL,
                min_percentage REAL NOT NULL,
                max_percentage REAL NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')

            self.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")
            return False

    def import_result_data(self, csv_path):
        """
        Import data from result.csv into the DSA table.

        Args:
            csv_path (str): Path to the result.csv file

        Returns:
            bool: True if import was successful, False otherwise
            int: Number of records imported
        """
        try:
            # Check if file exists
            if not os.path.exists(csv_path):
                print(f"File not found: {csv_path}")
                return False, 0

            # Only import if DSA table is empty
            self.execute_query("SELECT COUNT(*) FROM DSA")
            count = self.cursor.fetchone()[0]
            if count > 0:
                print("DSA table already contains data. Skipping import.")
                return False, 0

            # Read CSV file
            df = pd.read_csv(csv_path)

            # Process data: Calculate best 3 CT average and midterm scaled if not present
            if 'Best_3_CT_Avg' not in df.columns:
                ct_columns = ['CT1', 'CT2', 'CT3', 'CT4']
                ct_scores = []

                for _, row in df.iterrows():
                    scores = [row[col] for col in ct_columns if col in df.columns and pd.notna(row[col])]
                    scores.sort(reverse=True)
                    best_3_avg = sum(scores[:3]) / 3 if len(scores) >= 3 else (sum(scores) / len(scores) if scores else 0)
                    ct_scores.append(best_3_avg)

                df['Best_3_CT_Avg'] = ct_scores

            if 'Midterm_Scaled' not in df.columns and 'Mid-Term' in df.columns:
                df['Midterm_Scaled'] = df['Mid-Term'] / 2

            # Ensure required columns are present
            required_columns = ['Student Name', 'CT1', 'CT2', 'CT3', 'CT4', 'Mid-Term',
                                'Presentation', 'Attendance', 'Best_3_CT_Avg', 'Midterm_Scaled']

            for col in required_columns:
                if col not in df.columns:
                    if col in ['Best_3_CT_Avg', 'Midterm_Scaled']:
                        # Already handled above
                        continue
                    elif col == 'Attendance':
                        # Default attendance value
                        df[col] = 8
                    else:
                        # Default to 0 for missing columns
                        df[col] = 0

            # Calculate total and percentage if not present
            if 'Total_Obtained' not in df.columns:
                df['Total_Obtained'] = (
                    df['Midterm_Scaled'] +  # 20 marks
                    df['Best_3_CT_Avg'] +   # 10 marks
                    df['Presentation'] +    # 10 marks
                    df['Attendance']        # 10 marks
                )

            if 'Percentage' not in df.columns:
                df['Percentage'] = (df['Total_Obtained'] / 50) * 100

            # Calculate grade if not present
            if 'Grade' not in df.columns:
                def get_grade(percentage):
                    if percentage >= 80:
                        return 'A+'
                    elif percentage >= 75:
                        return 'A'
                    elif percentage >= 70:
                        return 'A-'
                    elif percentage >= 65:
                        return 'B+'
                    elif percentage >= 60:
                        return 'B'
                    elif percentage >= 55:
                        return 'B-'
                    elif percentage >= 50:
                        return 'C+'
                    elif percentage >= 45:
                        return 'C'
                    elif percentage >= 40:
                        return 'D'
                    else:
                        return 'F'

                df['Grade'] = df['Percentage'].apply(get_grade)

            # Calculate category if not present
            if 'Category' not in df.columns:
                def get_category(percentage):
                    if percentage >= 80:
                        return 'Excellent'
                    elif percentage >= 65:
                        return 'Good'
                    elif percentage >= 50:
                        return 'Average'
                    elif percentage >= 40:
                        return 'Below Average'
                    else:
                        return 'Poor'

                df['Category'] = df['Percentage'].apply(get_category)

            # Insert data into DSA table
            records_count = 0
            for _, row in df.iterrows():
                query = '''
                INSERT INTO DSA (
                    student_id, student_name, CT1, CT2, CT3, CT4, mid_term, 
                    presentation, attendance, best_3_CT_avg, midterm_scaled, 
                    total_obtained, percentage, grade, category
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                '''

                # Get student ID if it exists, otherwise use None
                student_id = row.get('StudentID', None)
                if pd.isna(student_id):
                    student_id = None

                params = (
                    student_id,
                    row['Student Name'],
                    row['CT1'],
                    row['CT2'],
                    row['CT3'],
                    row['CT4'],
                    row['Mid-Term'],
                    row['Presentation'],
                    row['Attendance'],
                    row['Best_3_CT_Avg'],
                    row['Midterm_Scaled'],
                    row['Total_Obtained'],
                    row['Percentage'],
                    row['Grade'],
                    row['Category']
                )

                self.execute_query(query, params)
                records_count += 1

            self.commit()
            return True, records_count
        except Exception as e:
            print(f"Error importing result data: {e}")
            return False, 0

    def import_grade_data(self):
        """
        Import grade data into the grade table.
        Since grade data is standardized, we'll insert it directly.

        Returns:
            bool: True if import was successful, False otherwise
        """
        try:
            # Clear existing data
            self.execute_query("DELETE FROM grade")

            # Define standard grade data
            grade_data = [
                ('A+', 80, 100, 'Excellent'),
                ('A', 75, 79.99, 'Very Good'),
                ('A-', 70, 74.99, 'Very Good'),
                ('B+', 65, 69.99, 'Good'),
                ('B', 60, 64.99, 'Good'),
                ('B-', 55, 59.99, 'Above Average'),
                ('C+', 50, 54.99, 'Average'),
                ('C', 45, 49.99, 'Below Average'),
                ('D', 40, 44.99, 'Pass'),
                ('F', 0, 39.99, 'Fail')
            ]

            # Insert grade data
            for grade, min_pct, max_pct, desc in grade_data:
                query = '''
                INSERT INTO grade (grade, min_percentage, max_percentage, description)
                VALUES (?, ?, ?, ?)
                '''
                self.execute_query(query, (grade, min_pct, max_pct, desc))

            self.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error importing grade data: {e}")
            return False

    def get_all_students(self):
        """
        Get all student records from the DSA table.

        Returns:
            list: List of student records as dictionaries
        """
        try:
            self.execute_query("SELECT * FROM DSA ORDER BY percentage DESC")
            columns = [desc[0] for desc in self.cursor.description]
            result = []
            for row in self.cursor.fetchall():
                result.append(dict(zip(columns, row)))
            return result
        except sqlite3.Error as e:
            print(f"Error retrieving students: {e}")
            return []

    def get_student_by_id(self, student_id):
        """
        Get a student record by ID.

        Args:
            student_id (str): Student ID to search for

        Returns:
            dict: Student record as a dictionary, or None if not found
        """
        try:
            self.execute_query("SELECT * FROM DSA WHERE student_id = ?", (student_id,))
            columns = [desc[0] for desc in self.cursor.description]
            row = self.cursor.fetchone()
            if row:
                return dict(zip(columns, row))
            return None
        except sqlite3.Error as e:
            print(f"Error retrieving student: {e}")
            return None

    def get_students_by_grade(self, grade):
        """
        Get all students with a specific grade.

        Args:
            grade (str): Grade to search for (e.g., 'A+', 'B', etc.)

        Returns:
            list: List of student records as dictionaries
        """
        try:
            self.execute_query("SELECT * FROM DSA WHERE grade = ? ORDER BY percentage DESC", (grade,))
            columns = [desc[0] for desc in self.cursor.description]
            result = []
            for row in self.cursor.fetchall():
                result.append(dict(zip(columns, row)))
            return result
        except sqlite3.Error as e:
            print(f"Error retrieving students by grade: {e}")
            return []

    def get_grade_info(self, grade=None):
        """
        Get grade information from the grade table.

        Args:
            grade (str, optional): Specific grade to get info for

        Returns:
            list or dict: List of grade records as dictionaries, or single dict if grade specified
        """
        try:
            if grade:
                self.execute_query("SELECT * FROM grade WHERE grade = ?", (grade,))
                columns = [desc[0] for desc in self.cursor.description]
                row = self.cursor.fetchone()
                if row:
                    return dict(zip(columns, row))
                return None
            else:
                self.execute_query("SELECT * FROM grade ORDER BY min_percentage DESC")
                columns = [desc[0] for desc in self.cursor.description]
                result = []
                for row in self.cursor.fetchall():
                    result.append(dict(zip(columns, row)))
                return result
        except sqlite3.Error as e:
            print(f"Error retrieving grade info: {e}")
            return [] if grade is None else None

    def get_statistics(self):
        """
        Get statistical information about the student results.

        Returns:
            dict: Dictionary containing statistical information
        """
        try:
            stats = {}

            # Total students
            self.execute_query("SELECT COUNT(*) FROM DSA")
            stats['total_students'] = self.cursor.fetchone()[0]

            # Average, max, min percentage
            self.execute_query("SELECT AVG(percentage), MAX(percentage), MIN(percentage) FROM DSA")
            avg, max_pct, min_pct = self.cursor.fetchone()
            stats['average_percentage'] = avg
            stats['highest_percentage'] = max_pct
            stats['lowest_percentage'] = min_pct

            # Grade distribution
            self.execute_query("""
                SELECT grade, COUNT(*) as count 
                FROM DSA 
                GROUP BY grade 
                ORDER BY MIN(percentage) DESC
            """)
            stats['grade_distribution'] = {grade: count for grade, count in self.cursor.fetchall()}

            # Category distribution
            self.execute_query("""
                SELECT category, COUNT(*) as count 
                FROM DSA 
                GROUP BY category 
                ORDER BY MIN(percentage) DESC
            """)
            stats['category_distribution'] = {category: count for category, count in self.cursor.fetchall()}

            return stats
        except sqlite3.Error as e:
            print(f"Error retrieving statistics: {e}")
            return {}
