import os

def get_project_root():
    """Get the root directory of the project"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(os.path.dirname(current_dir))

def get_data_dir():
    """Get the data directory path"""
    return os.path.join(get_project_root(), 'data')

def get_output_dir():
    """Get the output directory path"""
    return os.path.join(get_project_root(), 'output')

def resolve_file_path(file_path, base_dir=None):
    """
    Resolve a file path to an absolute path.
    If the path is relative, it will be resolved relative to the base_dir.
    If base_dir is not provided, it will use the project root.
    """
    if os.path.isabs(file_path):
        return file_path

    if base_dir is None:
        base_dir = get_project_root()

    # First try the provided path
    full_path = os.path.join(base_dir, file_path)
    if os.path.exists(full_path):
        return full_path

    # If not found, try in the data directory
    data_path = os.path.join(get_data_dir(), os.path.basename(file_path))
    if os.path.exists(data_path):
        return data_path

    raise FileNotFoundError(f"Could not find file: {file_path}")

def calculate_percentage(marks):
    total_marks = sum(marks)
    percentage = (total_marks / (len(marks) * 100)) * 100
    return percentage

def categorize_students(students):
    categories = {
        'Excellent': [],
        'Good': [],
        'Average': [],
        'Poor': []
    }
    
    for student in students:
        percentage = calculate_percentage(student['marks'])
        if percentage >= 85:
            categories['Excellent'].append(student)
        elif percentage >= 70:
            categories['Good'].append(student)
        elif percentage >= 50:
            categories['Average'].append(student)
        else:
            categories['Poor'].append(student)
    
    return categories

def load_csv_data(file_path):
    import pandas as pd
    data = pd.read_csv(file_path)
    return data.to_dict(orient='records')

def load_excel_data(file_path):
    import pandas as pd
    data = pd.read_excel(file_path)
    return data.to_dict(orient='records')