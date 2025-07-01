from sklearn.tree import DecisionTreeClassifier, plot_tree, export_text
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
import os
from src.utils.db_utils import DatabaseManager
from src.utils.helpers import get_output_dir

class ScholarshipService:
    def __init__(self):
        self.model = DecisionTreeClassifier(max_depth=4, min_samples_split=5)
        self.total_budget = 0
        # Database will be used to load student grades
        self.db_manager = DatabaseManager()
        self.scholarship_amounts = [0, 6000, 9000, 12000, 15000]  # Possible scholarship amounts

    def load_and_prepare_data(self):
        """Load and prepare data from the student_grades table in the database"""
        # Connect to database
        self.db_manager.connect()
        # Ensure student_grades table exists
        create_table = '''
        CREATE TABLE IF NOT EXISTS student_grades (
            student_id TEXT PRIMARY KEY,
            name TEXT,
            sgpa REAL,
            cgpa REAL
        )
        '''
        self.db_manager.execute_query(create_table)
        self.db_manager.connection.commit()
        query = "SELECT student_id AS Student_ID, name AS Name, sgpa AS SGPA FROM student_grades"
        df = pd.read_sql_query(query, self.db_manager.connection)
        self.db_manager.disconnect()

        # Ensure SGPA is numeric and valid
        df['SGPA'] = pd.to_numeric(df['SGPA'], errors='coerce')
        df = df.dropna(subset=['SGPA'])
        df = df[df['SGPA'] <= 4.0]

        # Add random monthly income between 10000 and 100000
        df['monthly_income'] = [random.randint(10000, 100000) for _ in range(len(df))]

        # Sort by SGPA in descending order
        df = df.sort_values('SGPA', ascending=False)

        # Normalize SGPA and monthly_income for better decision tree performance
        df['normalized_sgpa'] = (df['SGPA'] - df['SGPA'].min()) / (df['SGPA'].max() - df['SGPA'].min())
        df['normalized_income'] = (df['monthly_income'] - df['monthly_income'].min()) / (df['monthly_income'].max() - df['monthly_income'].min())

        print("\nSample of loaded student grades:")
        print(df[['Student_ID', 'Name', 'SGPA']].head())
        return df

    def prepare_training_data(self, data):
        """Prepare training data for the decision tree"""
        # Create target values based on rules
        y = []
        for _, row in data.iterrows():
            if row['SGPA'] >= 3.9:
                y.append(4)  # Index for 15000
            elif row['SGPA'] >= 3.8:
                y.append(3)  # Index for 9000
            elif row['SGPA'] >= 3.75 and row['monthly_income'] < 50000:
                y.append(2)  # Index for 12000
            elif row['SGPA'] >= 3.5 and row['monthly_income'] < 50000:
                y.append(1)  # Index for 6000
            else:
                y.append(0)  # Index for 0

        X = data[['normalized_sgpa', 'normalized_income']]
        return X, np.array(y)

    def train_model(self, X, y):
        """Train the decision tree model"""
        self.model.fit(X, y)

    def allocate_scholarships(self, total_budget):
        """Allocate scholarships using decision tree model"""
        self.total_budget = total_budget
        data = self.load_and_prepare_data()

        # Prepare and train the model
        X, y = self.prepare_training_data(data)
        self.train_model(X, y)

        # Make predictions
        predictions = self.model.predict(X)

        results = []
        total_allocated = 0

        # Convert predictions to actual scholarship amounts
        for i, row in data.iterrows():
            amount = self.scholarship_amounts[predictions[i]]

            # Check budget constraint
            if total_allocated + amount > total_budget:
                amount = 0

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

        # Save the decision tree visualization
        self.visualize_tree(X.columns)

        return pd.DataFrame(results)

    def visualize_tree(self, feature_names):
        """Visualize the decision tree and save it"""
        plt.figure(figsize=(20, 10))
        plot_tree(self.model, feature_names=feature_names,
                 class_names=[str(amt) for amt in self.scholarship_amounts],
                 filled=True, rounded=True)
        plt.title('Scholarship Decision Tree')

        # Save to output directory
        output_path = os.path.join(get_output_dir(), 'scholarship_decision_tree.png')
        os.makedirs(get_output_dir(), exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        # Also save tree rules as text
        tree_rules = export_text(self.model, feature_names=list(feature_names))
        rules_path = os.path.join(get_output_dir(), 'scholarship_tree_rules.txt')
        with open(rules_path, 'w') as f:
            f.write(tree_rules)

    def determine_scholarship_amount(self, sgpa, monthly_income):
        """
        Determine scholarship amount using the trained decision tree model.
        If model is not trained yet, falls back to rule-based decision.
        """
        # If model is not trained yet, use rule-based decision
        if not hasattr(self, 'model') or not hasattr(self.model, 'tree_'):
            print("\nUsing rule-based (if-else) decision making")
            if sgpa >= 3.9:
                return 15000
            elif sgpa >= 3.8:
                return 9000
            elif sgpa >= 3.75 and monthly_income < 50000:
                return 12000
            elif sgpa >= 3.5 and monthly_income < 50000:
                return 6000
            return 0

        print("\nUsing trained decision tree model for decision making")
        # Normalize input data similar to training data
        # Note: Using simple min-max scaling since this is for a single record
        normalized_sgpa = (sgpa - 0) / (4.0 - 0)  # SGPA is between 0-4
        normalized_income = (monthly_income - 10000) / (100000 - 10000)  # Income is between 10k-100k

        # Make prediction using the model
        X = np.array([[normalized_sgpa, normalized_income]])
        prediction = self.model.predict(X)[0]
        print(f"Input: SGPA={sgpa}, Income={monthly_income}")
        print(f"Normalized: SGPA={normalized_sgpa:.3f}, Income={normalized_income:.3f}")
        print(f"Model prediction index: {prediction}, Amount: {self.scholarship_amounts[prediction]} TK")

        return self.scholarship_amounts[prediction]
