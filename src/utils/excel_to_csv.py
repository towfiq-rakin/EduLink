import pandas as pd
import os

def convert_excel_to_csv():
    # Get file paths
    excel_path = os.path.join('data', 'CSE-23-3rd-Semester.xlsx')
    csv_path = os.path.join('data', 'student_grades.csv')

    try:
        # Read the Excel file
        df = pd.read_excel(excel_path)

        # Find the header row (where Student ID is)
        header_row = df[df['Unnamed: 3'] == 'Student ID'].index[0]

        # Read again with correct header
        df = pd.read_excel(excel_path, skiprows=header_row)

        # Extract relevant columns
        result_df = pd.DataFrame({
            'Student_ID': df['Unnamed: 3'],
            'Name': df['Unnamed: 4'],
            'SGPA': df['Unnamed: 66'],  # Current semester GPA
            'CGPA': df['Unnamed: 69']   # Cumulative GPA
        })

        # Clean the data
        result_df = result_df.dropna(subset=['SGPA', 'CGPA'])
        result_df['SGPA'] = pd.to_numeric(result_df['SGPA'], errors='coerce')
        result_df['CGPA'] = pd.to_numeric(result_df['CGPA'], errors='coerce')

        # Filter valid grades
        result_df = result_df[
            (result_df['SGPA'] > 0) &
            (result_df['SGPA'] <= 4.0) &
            (result_df['CGPA'] > 0) &
            (result_df['CGPA'] <= 4.0)
        ]

        # Save to CSV
        result_df.to_csv(csv_path, index=False)
        print(f"Data saved to {csv_path}")
        print("\nSample data:")
        print(result_df.head())
        print("\nData statistics:")
        print(result_df.describe())

        return True
    except Exception as e:
        print(f"Error converting file: {str(e)}")
        return False

if __name__ == "__main__":
    convert_excel_to_csv()
