import os
import pandas as pd
from src.utils.db_utils import DatabaseManager
from src.services.scholarship_service import ScholarshipService

def import_grades_to_db():
    # Initialize database manager
    db_manager = DatabaseManager()
    db_manager.connect()

    # Create grades table if it doesn't exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS student_grades (
        student_id TEXT PRIMARY KEY,
        name TEXT,
        sgpa REAL,
        cgpa REAL
    )
    """
    db_manager.execute_query(create_table_query)

    # Read CSV file
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    csv_path = os.path.join(base_path, 'data', 'student_grades.csv')
    grades_df = pd.read_csv(csv_path)

    # Insert data into database
    insert_query = """
    INSERT OR REPLACE INTO student_grades (student_id, name, sgpa, cgpa)
    VALUES (?, ?, ?, ?)
    """

    for _, row in grades_df.iterrows():
        params = (str(row['Student_ID']), row['Name'], row['SGPA'], row['CGPA'])
        db_manager.execute_query(insert_query, params)

    db_manager.connection.commit()
    db_manager.disconnect()

    print("Grades data imported successfully!")

    # Process scholarships and save allocations to database
    scholarship_service = ScholarshipService()
    total_budget = 1000000  # Setting budget to 1,000,000 (adjust as needed)
    results_df = scholarship_service.allocate_scholarships(total_budget)

    # Save scholarship allocations into DB
    db_manager.connect()
    create_alloc_table = """
    CREATE TABLE IF NOT EXISTS scholarship_allocations (
        student_id TEXT,
        name TEXT,
        sgpa REAL,
        monthly_income REAL,
        scholarship_amount REAL,
        allocated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    db_manager.execute_query(create_alloc_table)
    for _, row in results_df.iterrows():
        insert_alloc = """
        INSERT INTO scholarship_allocations (student_id, name, sgpa, monthly_income, scholarship_amount)
        VALUES (?, ?, ?, ?, ?)
        """
        params = (row['student_id'], row['name'], row['sgpa'], row['monthly_income'], row['scholarship_amount'])
        db_manager.execute_query(insert_alloc, params)
    db_manager.connection.commit()
    db_manager.disconnect()
    print("Scholarship allocations saved to database.")

if __name__ == "__main__":
    import_grades_to_db()
