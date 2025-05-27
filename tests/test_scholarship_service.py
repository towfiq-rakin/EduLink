import unittest
import sys
import os
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

# Add the project root directory to the Python path
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, project_root)

from src.services.scholarship_service import ScholarshipService

class TestScholarshipService(unittest.TestCase):
    """Test cases for ScholarshipService class"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.model = DecisionTreeClassifier()
        self.service = ScholarshipService(self.model)
        
        # Create sample data for testing
        self.sample_data = pd.DataFrame({
            'grade': [85, 90, 75, 95, 65],
            'attendance': [95, 98, 80, 99, 70],
            'extracurricular': [1, 1, 0, 1, 0],
            'scholarship_eligible': [1, 1, 0, 1, 0]
        })
    
    def test_model_training(self):
        """Test model training functionality"""
        features = self.sample_data[['grade', 'attendance', 'extracurricular']]
        target = self.sample_data['scholarship_eligible']
        
        self.service.train_model(features, target)
        self.assertTrue(hasattr(self.service.model, 'feature_importances_'))
    
    def test_scholarship_recommendation(self):
        """Test scholarship recommendation"""
        features = self.sample_data[['grade', 'attendance', 'extracurricular']]
        target = self.sample_data['scholarship_eligible']
        
        self.service.train_model(features, target)
        
        # Test recommendation for a high-performing student
        recommendation = self.service.recommend_scholarship([90, 95, 1])
        self.assertIsInstance(recommendation, (list, tuple))

if __name__ == "__main__":
    unittest.main()
