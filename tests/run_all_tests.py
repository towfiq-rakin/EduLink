"""
Script to run all tests in the EduLink project.
This script provides an easy way to execute all test suites.
"""
import unittest
import sys
import os

def discover_and_run_tests():
    """Discover and run all tests in the tests directory"""
    # Add the project root directory to the Python path
    project_root = os.path.join(os.path.dirname(__file__), '..')
    sys.path.insert(0, project_root)
    
    # Discover tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY:")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = discover_and_run_tests()
    sys.exit(0 if success else 1)
