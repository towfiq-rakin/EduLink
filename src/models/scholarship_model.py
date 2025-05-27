from sklearn.tree import DecisionTreeClassifier
import pandas as pd

class ScholarshipModel:
    def __init__(self):
        self.model = DecisionTreeClassifier()
        self.data = None

    def load_data(self, file_path):
        self.data = pd.read_csv(file_path)

    def train_model(self, features, target):
        if self.data is not None:
            X = self.data[features]
            y = self.data[target]
            self.model.fit(X, y)

    def recommend_scholarship(self, student_data):
        return self.model.predict([student_data])

    def get_feature_importance(self):
        return self.model.feature_importances_ if self.model else None

    def save_model(self, filename):
        import joblib
        joblib.dump(self.model, filename)

    def load_model(self, filename):
        import joblib
        self.model = joblib.load(filename)