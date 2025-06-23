import os
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from src.utils.helpers import get_data_dir, get_output_dir

class ScholarshipService:
    def __init__(self):
        self.model = DecisionTreeClassifier()
        self.total_budget = 0
        # Use the correct Excel file directly
        self.data_file = os.path.join(get_data_dir(), 'CSE-23-3rd-Semester.xlsx')

    def load_and_prepare_data(self):
        """Load and prepare data directly from Excel file"""
        try:
            # Read the raw Excel file
            df = pd.read_excel(self.data_file)

            # Find the header row
            header_row = df[df['Unnamed: 3'] == 'Student ID'].index[0]

            # Read Excel file again with correct header
            df = pd.read_excel(self.data_file, skiprows=header_row)

            # Create clean DataFrame with required columns
            processed_df = pd.DataFrame({
                'Student_ID': df['Unnamed: 3'],
                'Name': df['Unnamed: 4'],
                'SGPA': pd.to_numeric(df['Unnamed: 66'], errors='coerce'),  # Current semester GPA
            })

            # Remove any rows with invalid SGPA
            processed_df = processed_df.dropna(subset=['SGPA'])
            processed_df = processed_df[processed_df['SGPA'] <= 4.0]

            # Add random monthly income between 10000 and 100000
            processed_df['monthly_income'] = [random.randint(10000, 100000) for _ in range(len(processed_df))]

            # Sort by SGPA in descending order to process higher grades first
            processed_df = processed_df.sort_values('SGPA', ascending=False)

            print("\nProcessed data sample:")
            print(processed_df[['Student_ID', 'Name', 'SGPA']].head())
            return processed_df

        except Exception as e:
            raise ValueError(f"Error processing Excel file: {str(e)}")

    def determine_scholarship_amount(self, sgpa, monthly_income):
        """
        Determine scholarship amount based on SGPA and income.
        Rules:
        1. SGPA 3.9 or higher: 15000 tk (no income check)
        2. SGPA 3.8 or higher: 9000 tk (no income check)
        3. SGPA 3.75 or higher: 12000 tk (with income check)
        4. SGPA 3.5 or higher: 6000 tk (with income check)
        """
        # First process scholarships without income consideration
        if sgpa >= 3.9:
            return 15000
        elif sgpa >= 3.8:
            return 9000

        # Then process scholarships with income consideration
        if monthly_income < 50000:
            if sgpa >= 3.75:
                return 12000
            elif sgpa >= 3.5:
                return 6000

        return 0

    def allocate_scholarships(self, total_budget):
        """Allocate scholarships based on fixed amounts without exceeding total budget"""
        self.total_budget = total_budget
        data = self.load_and_prepare_data()
        results = []
        total_allocated = 0

        # Calculate allocations with fixed amounts and budget limit
        for _, row in data.iterrows():
            amount = self.determine_scholarship_amount(row['SGPA'], row['monthly_income'])

            # Check if adding this scholarship would exceed budget
            if total_allocated + amount > total_budget:
                amount = 0  # Don't award if it would exceed budget

            total_allocated += amount

            results.append({
                'student_id': row['Student_ID'],
                'name': row['Name'],
                'sgpa': row['SGPA'],
                'monthly_income': row['monthly_income'],
                'scholarship_amount': amount
            })

        print(f"\nTotal budget: {total_budget:,} TK")
        print(f"Total allocated: {total_allocated:,} TK")
        print(f"Remaining budget: {total_budget - total_allocated:,} TK")

        return pd.DataFrame(results)

    def visualize_distribution(self, results):
        """Create visualization of scholarship distribution"""
        plt.figure(figsize=(12, 6))

        # Create scholarship amount distribution
        scholarship_counts = results[results['scholarship_amount'] > 0]['scholarship_amount'].value_counts()

        plt.bar(scholarship_counts.index.astype(str), scholarship_counts.values)
        plt.title('Scholarship Distribution')
        plt.xlabel('Scholarship Amount (TK)')
        plt.ylabel('Number of Recipients')
        plt.xticks(rotation=45)

        plt.tight_layout()

        # Save to output directory
        output_path = os.path.join(get_output_dir(), 'scholarship_distribution.png')
        os.makedirs(get_output_dir(), exist_ok=True)
        plt.savefig(output_path)
        plt.close()

        return output_path
