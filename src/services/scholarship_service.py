from sklearn.tree import DecisionTreeClassifier
import pandas as pd

class ScholarshipService:
    def __init__(self, model):
        self.model = model

    def train_model(self, data, target):
        self.model.fit(data, target)

    def recommend_scholarship(self, student_data):
        prediction = self.model.predict([student_data])
        return prediction

    def load_data(self, file_path):
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            return pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format. Please provide a CSV or Excel file.")

    def preprocess_data(self, data):
        # Implement any necessary preprocessing steps here
        return data