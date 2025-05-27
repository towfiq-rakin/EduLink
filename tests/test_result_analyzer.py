import unittest
import sys
import os

# Add the project root directory to the Python path
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, project_root)

from src.services.result_analyzer import ResultAnalyzer

class TestResultAnalyzer(unittest.TestCase):
    """Test cases for ResultAnalyzer class"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.dataset_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'result.csv')
        self.analyzer = ResultAnalyzer(self.dataset_path)
    
    def test_data_loading(self):
        """Test if data loads successfully"""
        result = self.analyzer.load_data()
        self.assertTrue(result, "Data should load successfully")
        self.assertIsNotNone(self.analyzer.data, "Data should not be None after loading")
    
    def test_data_preprocessing(self):
        """Test data preprocessing functionality"""
        if self.analyzer.load_data():
            processed_data = self.analyzer.preprocess_data()
            self.assertIsNotNone(processed_data, "Processed data should not be None")
    
    def test_percentage_calculation(self):
        """Test percentage calculation"""
        if self.analyzer.load_data():
            self.analyzer.preprocess_data()
            result_data = self.analyzer.calculate_total_and_percentage()
            self.assertIn('Percentage', result_data.columns, "Percentage column should exist")
            self.assertIn('Total_Obtained', result_data.columns, "Total_Obtained column should exist")
    
    def test_student_categorization(self):
        """Test student categorization"""
        if self.analyzer.load_data():
            self.analyzer.preprocess_data()
            self.analyzer.calculate_total_and_percentage()
            categorized_data = self.analyzer.categorize_students()
            self.assertIn('Category', categorized_data.columns, "Category column should exist")
            self.assertIn('Grade', categorized_data.columns, "Grade column should exist")
    
    def test_report_generation(self):
        """Test report generation"""
        if self.analyzer.load_data():
            self.analyzer.preprocess_data()
            self.analyzer.calculate_total_and_percentage()
            self.analyzer.categorize_students()
            report = self.analyzer.generate_detailed_report()
            self.assertIsInstance(report, dict, "Report should be a dictionary")
            self.assertIn('total_students', report, "Report should contain total_students")

def run_comprehensive_test():
    """Run comprehensive test with detailed output"""
    print("="*80)
    print("EDULINK - RESULT ANALYZER TEST")
    print("="*80)
    
    # Use the dataset from data directory
    dataset_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'result.csv')
    
    # Create analyzer instance
    analyzer = ResultAnalyzer(dataset_path)
    
    # Load and process data
    if analyzer.load_data():
        print("✓ Data loaded successfully!")
        
        # Process the data
        analyzer.preprocess_data()
        print("✓ Data preprocessing completed!")
        
        analyzer.calculate_total_and_percentage()
        print("✓ Percentage calculation completed!")
        
        analyzer.categorize_students()
        print("✓ Student categorization completed!")
        
        # Print report to terminal
        analyzer.print_report_to_terminal()
        
        # Save report to file
        filename = analyzer.save_report_to_file()
        print(f"\n✓ Detailed report saved to: {filename}")
        
        # Display individual student results
        print("\n" + "="*80)
        print("INDIVIDUAL STUDENT RESULTS:")
        print("="*80)
        student_results = analyzer.get_student_results()
        print(student_results.to_string(index=False))
        
        print("\n✓ All tests completed successfully!")
        
    else:
        print("✗ Failed to load data. Please check the file path.")

if __name__ == "__main__":
    # You can run either unit tests or comprehensive test
    import argparse
    parser = argparse.ArgumentParser(description='Run tests for ResultAnalyzer')
    parser.add_argument('--mode', choices=['unit', 'comprehensive'], default='comprehensive',
                       help='Test mode: unit for unittest, comprehensive for full test')
    args = parser.parse_args()
    
    if args.mode == 'unit':
        unittest.main()
    else:
        run_comprehensive_test()
