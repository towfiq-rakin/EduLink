import pandas as pd
import numpy as np
from datetime import datetime

class ResultAnalyzer:
    def __init__(self, data_file):
        self.data_file = data_file
        self.data = None
        self.processed_data = None

    def load_data(self):
        """Load data from CSV or Excel file"""
        try:
            if self.data_file.endswith('.csv'):
                self.data = pd.read_csv(self.data_file)
            elif self.data_file.endswith(('.xls', '.xlsx')):
                self.data = pd.read_excel(self.data_file)
            else:
                raise ValueError("Unsupported file format. Please provide a CSV or Excel file.")
            print(f"Data loaded successfully from {self.data_file}")
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False

    def preprocess_data(self):
        """Clean and preprocess the data"""
        if self.data is None:
            raise ValueError("Data not loaded. Please load the data first.")
        
        # Create a copy for processing
        self.processed_data = self.data.copy()
        
        # Handle 'A' (Absent) marks - replace with 0
        mark_columns = ['CT1', 'CT2', 'Mid-Term', 'CT3', 'CT4', 'Presentation']
        for col in mark_columns:
            if col in self.processed_data.columns:
                self.processed_data[col] = pd.to_numeric(self.processed_data[col], errors='coerce').fillna(0)
        
        return self.processed_data

    def calculate_total_and_percentage(self):
        """Calculate total marks and percentage for each student"""
        if self.processed_data is None:
            self.preprocess_data()
        
        # New grading system:
        # - Mid-term: 20 marks (scaled from 40 to 20)
        # - Best 3 CTs average: 10 marks 
        # - Presentation: 10 marks
        # - Attendance: 10 marks
        # Total: 50 marks
        
        # Calculate scaled midterm marks (half of original)
        self.processed_data['Midterm_Scaled'] = self.processed_data['Mid-Term'] / 2
        
        # Calculate best 3 CT average
        ct_columns = ['CT1', 'CT2', 'CT3', 'CT4']
        ct_scores = []
        
        for index, row in self.processed_data.iterrows():
            # Get CT scores for this student
            scores = [row[col] for col in ct_columns if col in self.processed_data.columns and pd.notna(row[col])]
            # Sort and take best 3
            scores.sort(reverse=True)
            best_3_avg = sum(scores[:3]) / 3 if len(scores) >= 3 else (sum(scores) / len(scores) if scores else 0)
            ct_scores.append(best_3_avg)
        
        self.processed_data['Best_3_CT_Avg'] = ct_scores
        
        # Calculate total marks obtained (out of 50)
        self.processed_data['Total_Obtained'] = (
            self.processed_data['Midterm_Scaled'] +  # 20 marks
            self.processed_data['Best_3_CT_Avg'] +   # 10 marks
            self.processed_data['Presentation'] +    # 10 marks
            self.processed_data['Attendance']        # 10 marks
        )
        
        # Calculate percentage (out of 50)
        self.processed_data['Percentage'] = (self.processed_data['Total_Obtained'] / 50) * 100
        
        return self.processed_data

    def categorize_students(self):
        """Categorize students based on their performance"""
        if 'Percentage' not in self.processed_data.columns:
            self.calculate_total_and_percentage()
        
        def get_grade(percentage):
            if percentage >= 80:
                return 'A+'
            elif percentage >= 75:
                return 'A'
            elif percentage >= 70:
                return 'A-'
            elif percentage >= 65:
                return 'B+'
            elif percentage >= 60:
                return 'B'
            elif percentage >= 55:
                return 'B-'
            elif percentage >= 50:
                return 'C+'
            elif percentage >= 45:
                return 'C'
            elif percentage >= 40:
                return 'D'
            else:
                return 'F'
        
        def get_category(percentage):
            if percentage >= 80:
                return 'Excellent'
            elif percentage >= 65:
                return 'Good'
            elif percentage >= 50:
                return 'Average'
            elif percentage >= 40:
                return 'Below Average'
            else:
                return 'Poor'
        
        self.processed_data['Grade'] = self.processed_data['Percentage'].apply(get_grade)
        self.processed_data['Category'] = self.processed_data['Percentage'].apply(get_category)
        
        return self.processed_data

    def generate_detailed_report(self):
        """Generate a comprehensive analysis report"""
        if self.processed_data is None:
            self.categorize_students()
        
        report = {}
        
        # Basic statistics
        report['total_students'] = len(self.processed_data)
        report['average_percentage'] = self.processed_data['Percentage'].mean()
        report['highest_percentage'] = self.processed_data['Percentage'].max()
        report['lowest_percentage'] = self.processed_data['Percentage'].min()
        report['median_percentage'] = self.processed_data['Percentage'].median()
        
        # Category-wise distribution
        category_distribution = self.processed_data['Category'].value_counts().to_dict()
        report['category_distribution'] = category_distribution
        
        # Grade-wise distribution
        grade_distribution = self.processed_data['Grade'].value_counts().to_dict()
        report['grade_distribution'] = grade_distribution
        
        # Top performers
        top_performers = self.processed_data.nlargest(5, 'Percentage')[['Student Name', 'Percentage', 'Grade']].to_dict('records')
        report['top_performers'] = top_performers
        
        # Students needing attention (bottom 5)
        bottom_performers = self.processed_data.nsmallest(5, 'Percentage')[['Student Name', 'Percentage', 'Grade']].to_dict('records')
        report['students_needing_attention'] = bottom_performers
        
        # Subject-wise analysis (updated for new system)
        subject_analysis = {}
        
        # Individual CT analysis
        mark_columns = ['CT1', 'CT2', 'CT3', 'CT4']
        for col in mark_columns:
            if col in self.processed_data.columns:
                subject_analysis[col] = {
                    'average': self.processed_data[col].mean(),
                    'highest': self.processed_data[col].max(),
                    'lowest': self.processed_data[col].min(),
                    'students_with_zero': (self.processed_data[col] == 0).sum()
                }
        
        # Best 3 CT average analysis
        subject_analysis['Best_3_CT_Average'] = {
            'average': self.processed_data['Best_3_CT_Avg'].mean(),
            'highest': self.processed_data['Best_3_CT_Avg'].max(),
            'lowest': self.processed_data['Best_3_CT_Avg'].min(),
            'students_with_zero': (self.processed_data['Best_3_CT_Avg'] == 0).sum()
        }
        
        # Midterm (original and scaled)
        subject_analysis['Mid-Term_Original'] = {
            'average': self.processed_data['Mid-Term'].mean(),
            'highest': self.processed_data['Mid-Term'].max(),
            'lowest': self.processed_data['Mid-Term'].min(),
            'students_with_zero': (self.processed_data['Mid-Term'] == 0).sum()
        }
        
        subject_analysis['Mid-Term_Scaled'] = {
            'average': self.processed_data['Midterm_Scaled'].mean(),
            'highest': self.processed_data['Midterm_Scaled'].max(),
            'lowest': self.processed_data['Midterm_Scaled'].min(),
            'students_with_zero': (self.processed_data['Midterm_Scaled'] == 0).sum()
        }
        
        # Presentation and Attendance
        for col in ['Presentation', 'Attendance']:
            if col in self.processed_data.columns:
                subject_analysis[col] = {
                    'average': self.processed_data[col].mean(),
                    'highest': self.processed_data[col].max(),
                    'lowest': self.processed_data[col].min(),
                    'students_with_zero': (self.processed_data[col] == 0).sum()
                }
        
        report['subject_analysis'] = subject_analysis
        
        return report

    def save_report_to_file(self, filename=None):
        """Save the detailed report to a text file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"result_analysis_report_{timestamp}.txt"
        
        report = self.generate_detailed_report()
        
        with open(filename, 'w') as f:
            f.write("="*80 + "\n")
            f.write("EDULINK - RESULT ANALYSIS REPORT\n")
            f.write("="*80 + "\n\n")
            
            f.write("GRADING SYSTEM:\n")
            f.write("-"*40 + "\n")
            f.write("• Mid-term: 20 marks (scaled from 40)\n")
            f.write("• Best 3 CT Average: 10 marks\n")
            f.write("• Presentation: 10 marks\n")
            f.write("• Attendance: 10 marks\n")
            f.write("• Total: 50 marks\n\n")
            
            # Basic Statistics
            f.write("BASIC STATISTICS:\n")
            f.write("-"*40 + "\n")
            f.write(f"Total Students: {report['total_students']}\n")
            f.write(f"Average Percentage: {report['average_percentage']:.2f}%\n")
            f.write(f"Highest Percentage: {report['highest_percentage']:.2f}%\n")
            f.write(f"Lowest Percentage: {report['lowest_percentage']:.2f}%\n")
            f.write(f"Median Percentage: {report['median_percentage']:.2f}%\n\n")
            
            # Category Distribution
            f.write("CATEGORY DISTRIBUTION:\n")
            f.write("-"*40 + "\n")
            for category, count in report['category_distribution'].items():
                percentage_of_total = (count / report['total_students']) * 100
                f.write(f"{category}: {count} students ({percentage_of_total:.1f}%)\n")
            f.write("\n")
            
            # Grade Distribution
            f.write("GRADE DISTRIBUTION:\n")
            f.write("-"*40 + "\n")
            for grade, count in sorted(report['grade_distribution'].items()):
                percentage_of_total = (count / report['total_students']) * 100
                f.write(f"Grade {grade}: {count} students ({percentage_of_total:.1f}%)\n")
            f.write("\n")
            
            # Top Performers
            f.write("TOP 5 PERFORMERS:\n")
            f.write("-"*40 + "\n")
            for i, student in enumerate(report['top_performers'], 1):
                f.write(f"{i}. {student['Student Name']} - {student['Percentage']:.2f}% (Grade: {student['Grade']})\n")
            f.write("\n")
            
            # Students Needing Attention
            f.write("STUDENTS NEEDING ATTENTION (Bottom 5):\n")
            f.write("-"*50 + "\n")
            for i, student in enumerate(report['students_needing_attention'], 1):
                f.write(f"{i}. {student['Student Name']} - {student['Percentage']:.2f}% (Grade: {student['Grade']})\n")
            f.write("\n")
            
            # ALL STUDENTS RESULTS
            f.write("ALL STUDENTS RESULTS:\n")
            f.write("="*90 + "\n")
            student_results = self.get_student_results()
            f.write(f"{'No.':<4} {'Student Name':<35} {'CT Avg':<8} {'Mid':<6} {'Pres':<6} {'Att':<4} {'Total':<6} {'%':<6} {'Grade':<6}\n")
            f.write("-"*90 + "\n")
            
            for i, (_, student) in enumerate(student_results.iterrows(), 1):
                f.write(f"{i:<4} {student['Student Name']:<35} {student['Best_3_CT_Avg']:<8.2f} "
                       f"{student['Midterm_Scaled']:<6.1f} {student['Presentation']:<6.1f} "
                       f"{student['Attendance']:<4.0f} {student['Total_Obtained']:<6.1f} "
                       f"{student['Percentage']:<6.2f} {student['Grade']:<6}\n")
            f.write("\n")
            
            # Subject-wise Analysis
            f.write("RESULT-WISE ANALYSIS:\n")
            f.write("-"*40 + "\n")
            for subject, stats in report['subject_analysis'].items():
                f.write(f"\n{subject}:\n")
                f.write(f"  Average: {stats['average']:.2f}\n")
                f.write(f"  Highest: {stats['highest']:.2f}\n")
                f.write(f"  Lowest: {stats['lowest']:.2f}\n")
                f.write(f"  Absent/Zero marks: {stats['students_with_zero']} students\n")
            
            f.write("\n" + "="*80 + "\n")
            f.write(f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n")
        
        print(f"Report saved to: {filename}")
        return filename

    def print_report_to_terminal(self):
        """Print the report to terminal"""
        report = self.generate_detailed_report()
        
        print("="*80)
        print("EDULINK - RESULT ANALYSIS REPORT")
        print("="*80)
        
        print("\nGRADING SYSTEM:")
        print("-"*40)
        print("• Mid-term: 20 marks (scaled from 40)")
        print("• Best 3 CT Average: 10 marks")
        print("• Presentation: 10 marks")
        print("• Attendance: 10 marks")
        print("• Total: 50 marks")
        
        # Basic Statistics
        print("\nBASIC STATISTICS:")
        print("-"*40)
        print(f"Total Students: {report['total_students']}")
        print(f"Average Percentage: {report['average_percentage']:.2f}%")
        print(f"Highest Percentage: {report['highest_percentage']:.2f}%")
        print(f"Lowest Percentage: {report['lowest_percentage']:.2f}%")
        print(f"Median Percentage: {report['median_percentage']:.2f}%")
        
        # Category Distribution
        print("\nCATEGORY DISTRIBUTION:")
        print("-"*40)
        for category, count in report['category_distribution'].items():
            percentage_of_total = (count / report['total_students']) * 100
            print(f"{category}: {count} students ({percentage_of_total:.1f}%)")
        
        # Grade Distribution
        print("\nGRADE DISTRIBUTION:")
        print("-"*40)
        for grade, count in sorted(report['grade_distribution'].items()):
            percentage_of_total = (count / report['total_students']) * 100
            print(f"Grade {grade}: {count} students ({percentage_of_total:.1f}%)")
        
        # Top Performers
        print("\nTOP 5 PERFORMERS:")
        print("-"*40)
        for i, student in enumerate(report['top_performers'], 1):
            print(f"{i}. {student['Student Name']} - {student['Percentage']:.2f}% (Grade: {student['Grade']})")
        
        # Students Needing Attention
        print("\nSTUDENTS NEEDING ATTENTION (Bottom 5):")
        print("-"*50)
        for i, student in enumerate(report['students_needing_attention'], 1):
            print(f"{i}. {student['Student Name']} - {student['Percentage']:.2f}% (Grade: {student['Grade']})")
        
        # ALL STUDENTS RESULTS
        print("\nALL STUDENTS RESULTS:")
        print("="*80)
        student_results = self.get_student_results()
        print(f"{'No.':<4} {'Student Name':<35} {'CT Avg':<8} {'Mid':<6} {'Pres':<6} {'Att':<4} {'Total':<6} {'%':<6} {'Grade':<6}")
        print("-"*80)
        
        for i, (_, student) in enumerate(student_results.iterrows(), 1):
            print(f"{i:<4} {student['Student Name']:<35} {student['Best_3_CT_Avg']:<8.2f} "
                 f"{student['Midterm_Scaled']:<6.1f} {student['Presentation']:<6.1f} "
                 f"{student['Attendance']:<4.0f} {student['Total_Obtained']:<6.1f} "
                 f"{student['Percentage']:<6.2f} {student['Grade']:<6}")
        
        # Subject-wise Analysis
        print("\nSUBJECT-WISE ANALYSIS:")
        print("-"*40)
        for subject, stats in report['subject_analysis'].items():
            print(f"\n{subject}:")
            print(f"  Average: {stats['average']:.2f}")
            print(f"  Highest: {stats['highest']:.2f}")
            print(f"  Lowest: {stats['lowest']:.2f}")
            print(f"  Absent/Zero marks: {stats['students_with_zero']} students")
        
        print("\n" + "="*80)

    def get_student_results(self):
        """Get processed results for all students"""
        if self.processed_data is None:
            self.categorize_students()
        
        return self.processed_data[['Student Name', 'Best_3_CT_Avg', 'Midterm_Scaled', 'Presentation', 'Attendance', 'Total_Obtained', 'Percentage', 'Grade', 'Category']]

    # Keep the old methods for backward compatibility
    def calculate_percentages(self):
        """Legacy method - use calculate_total_and_percentage() instead"""
        return self.calculate_total_and_percentage()

    def generate_report(self):
        """Legacy method - use generate_detailed_report() instead"""
        if self.processed_data is not None:
            report = self.processed_data.groupby('Category').size().reset_index(name='Count')
            return report
        else:
            raise ValueError("Data not loaded. Please load the data first.")