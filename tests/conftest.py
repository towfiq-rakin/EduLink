"""
Pytest configuration file for EduLink tests.
This file contains shared fixtures and configuration for all tests.
"""
import pytest
import sys
import os

# Add the project root directory to the Python path for all tests
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, project_root)

@pytest.fixture
def sample_dataset_path():
    """Fixture providing the path to the sample dataset"""
    return os.path.join(os.path.dirname(__file__), '..', 'data', 'result.csv')

@pytest.fixture
def test_data_dir():
    """Fixture providing the test data directory path"""
    return os.path.join(os.path.dirname(__file__), '..', 'data')
