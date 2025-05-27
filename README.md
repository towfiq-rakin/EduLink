# EduLink Project

EduLink is a student management application designed for teachers, focusing on two major functionalities: a scholarship management system and a result analysis tool. 

## Features

1. **Scholarship Management System**: 
   - Provides recommendations for scholarships based on student data using decision tree algorithms implemented with libraries such as NumPy and scikit-learn.

2. **Result Analysis Tool**: 
   - Analyzes student results from CSV or Excel files.
   - Generates comprehensive reports including percentages and categorization of students based on their performance.

## GUI

The application utilizes customTkinter for a user-friendly graphical interface, allowing users to easily navigate through the scholarship management and result analysis features.

## Project Structure

```
EduLink
├── src
│   ├── main.py                  # Entry point of the application
│   ├── gui                      # GUI components
│   │   ├── __init__.py
│   │   ├── main_window.py       # Main application window
│   │   ├── scholarship_window.py # Scholarship management interface
│   │   └── result_window.py     # Result analysis interface
│   ├── models                   # Data models
│   │   ├── __init__.py
│   │   ├── scholarship_model.py  # Scholarship data structure and logic
│   │   └── result_model.py      # Student results data structure
│   ├── services                 # Business logic
│   │   ├── __init__.py
│   │   ├── scholarship_service.py # Scholarship management logic
│   │   ├── result_analyzer.py   # Result analysis logic
│   │   └── data_processor.py     # Data processing for CSV/Excel files
│   └── utils                    # Utility functions
│       ├── __init__.py
│       └── helpers.py           # Helper functions
├── tests                        # Test suite
│   ├── __init__.py
│   ├── test_result_analyzer.py  # Tests for result analyzer
│   ├── test_scholarship_service.py # Tests for scholarship service
│   ├── test_data_processor.py   # Tests for data processor
│   ├── conftest.py             # Pytest configuration
│   └── run_all_tests.py        # Script to run all tests
├── data
│   └── sample_data.csv          # Sample data for testing
├── requirements.txt             # Project dependencies
└── README.md                    # Project documentation
```

## Installation

To set up the project, clone the repository and install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the application by executing the main script:

```bash
python src/main.py
```

This will launch the GUI, where you can manage scholarships and analyze student results.

## Testing

The project includes a comprehensive test suite located in the `tests` directory.

### Running Tests

To run all tests:
```bash
python tests/run_all_tests.py
```

To run specific test modules:
```bash
python tests/test_result_analyzer.py
python tests/test_scholarship_service.py
python tests/test_data_processor.py
```

To run tests with pytest (if installed):
```bash
pytest tests/
```

To run the comprehensive result analyzer test:
```bash
python tests/test_result_analyzer.py --mode comprehensive
```

### Test Coverage

The test suite covers:
- Result analysis functionality
- Data loading and processing
- Scholarship recommendation system
- Data validation and error handling

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements. 

When contributing, please:
1. Add tests for new functionality
2. Ensure all existing tests pass
3. Follow the existing code style

## License

This project is licensed under the MIT License.