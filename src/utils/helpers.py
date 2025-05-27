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