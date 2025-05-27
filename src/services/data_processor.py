import pandas as pd

class DataProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def load_data(self):
        if self.file_path.endswith('.csv'):
            self.data = pd.read_csv(self.file_path)
        elif self.file_path.endswith(('.xls', '.xlsx')):
            self.data = pd.read_excel(self.file_path)
        else:
            raise ValueError("Unsupported file format. Please provide a CSV or Excel file.")

    def get_data_summary(self):
        if self.data is not None:
            return self.data.describe()
        else:
            raise ValueError("No data loaded. Please load data using load_data() method.")

    def filter_data(self, criteria):
        if self.data is not None:
            return self.data.query(criteria)
        else:
            raise ValueError("No data loaded. Please load data using load_data() method.")

    def save_processed_data(self, output_path):
        if self.data is not None:
            self.data.to_csv(output_path, index=False)
        else:
            raise ValueError("No data to save. Please load and process data first.")