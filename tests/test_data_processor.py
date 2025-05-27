import unittest
import sys
import os
import tempfile
import pandas as pd

# Add the project root directory to the Python path
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, project_root)

from src.services.data_processor import DataProcessor

class TestDataProcessor(unittest.TestCase):
    """Test cases for DataProcessor class"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        # Create a temporary CSV file for testing
        self.test_data = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie'],
            'grade': [85, 90, 75],
            'attendance': [95, 98, 80]
        })
        
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        self.test_data.to_csv(self.temp_file.name, index=False)
        self.temp_file.close()
        
        self.processor = DataProcessor(self.temp_file.name)
    
    def tearDown(self):
        """Clean up after each test method"""
        os.unlink(self.temp_file.name)
    
    def test_data_loading(self):
        """Test data loading functionality"""
        self.processor.load_data()
        self.assertIsNotNone(self.processor.data)
        self.assertEqual(len(self.processor.data), 3)
    
    def test_data_summary(self):
        """Test data summary generation"""
        self.processor.load_data()
        summary = self.processor.get_data_summary()
        self.assertIsNotNone(summary)

if __name__ == "__main__":
    unittest.main()
