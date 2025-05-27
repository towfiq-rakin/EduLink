class ResultModel:
    def __init__(self, student_data):
        self.student_data = student_data  # List of dictionaries containing student information

    def calculate_percentage(self):
        for student in self.student_data:
            total_marks = sum(student['marks'])
            percentage = (total_marks / (len(student['marks']) * 100)) * 100
            student['percentage'] = percentage

    def categorize_students(self):
        categories = {
            'A': [],
            'B': [],
            'C': [],
            'D': []
        }
        for student in self.student_data:
            if student.get('percentage', 0) >= 75:
                categories['A'].append(student)
            elif student.get('percentage', 0) >= 50:
                categories['B'].append(student)
            elif student.get('percentage', 0) >= 35:
                categories['C'].append(student)
            else:
                categories['D'].append(student)
        return categories

    def generate_report(self):
        self.calculate_percentage()
        categorized_students = self.categorize_students()
        report = {
            'total_students': len(self.student_data),
            'categories': categorized_students
        }
        return report