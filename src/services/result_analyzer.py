import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import os

class ResultAnalyzer:
    def __init__(self, data_file):
        self.data_file = os.path.normpath(data_file)  # Normalize path
        self.data = None
        self.processed_data = None
        # Use os.path.abspath to get absolute path and normalize it
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.output_dir = os.path.join(root_dir, 'output')
        os.makedirs(self.output_dir, exist_ok=True)

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
        
        self.processed_data = self.data.copy()

        
        mark_columns = ['CT1', 'CT2', 'Mid-Term', 'CT3', 'CT4', 'Presentation', 'Attendance']
        for col in mark_columns:
            if col in self.processed_data.columns:
                self.processed_data[col] = pd.to_numeric(self.processed_data[col], errors='coerce').fillna(0)
        
        return self.processed_data

    def calculate_total_and_percentage(self):
        """Calculate total marks and percentage for each student"""
        if self.processed_data is None:
            self.preprocess_data()
        
        # Scale Mid-Term from 40 to 20
        self.processed_data['Midterm_Scaled'] = self.processed_data['Mid-Term'] / 2
        
        ct_columns = ['CT1', 'CT2', 'CT3', 'CT4']
        ct_scores = []
        
        for index, row in self.processed_data.iterrows():
            scores = [row[col] for col in ct_columns if col in self.processed_data.columns and pd.notna(row[col])]
            scores.sort(reverse=True)
            best_3_avg = sum(scores[:3]) / 3 if len(scores) >= 3 else (sum(scores) / len(scores) if scores else 0)
            ct_scores.append(best_3_avg)
        
        self.processed_data['Best_3_CT_Avg'] = ct_scores
        
        # Ensure all required columns exist before calculation
        for col in ['Midterm_Scaled', 'Best_3_CT_Avg', 'Presentation', 'Attendance']:
            if col not in self.processed_data.columns:
                if col == 'Attendance':
                    self.processed_data[col] = 8  # Default value
                else:
                    self.processed_data[col] = 0  # Default value
        
        self.processed_data['Total_Obtained'] = (
            self.processed_data['Midterm_Scaled'] +  # 20 marks
            self.processed_data['Best_3_CT_Avg'] +   # 10 marks
            self.processed_data['Presentation'] +    # 10 marks
            self.processed_data['Attendance']        # 10 marks
        )
        
        self.processed_data['Percentage'] = (self.processed_data['Total_Obtained'] / 50) * 100
        
        return self.processed_data

    def categorize_students(self):
        """Categorize students based on their performance"""
        if self.processed_data is None:
            self.preprocess_data()
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
        
        report['total_students'] = len(self.processed_data)
        report['average_percentage'] = self.processed_data['Percentage'].mean()
        report['highest_percentage'] = self.processed_data['Percentage'].max()
        report['lowest_percentage'] = self.processed_data['Percentage'].min()
        report['median_percentage'] = self.processed_data['Percentage'].median()
        
        category_distribution = self.processed_data['Category'].value_counts().to_dict()
        report['category_distribution'] = category_distribution
        
        grade_distribution = self.processed_data['Grade'].value_counts().to_dict()
        report['grade_distribution'] = grade_distribution
        
        top_performers = self.processed_data.nlargest(5, 'Percentage')[['Student Name', 'Percentage', 'Grade']].to_dict('records')
        report['top_performers'] = top_performers
        
        bottom_performers = self.processed_data.nsmallest(5, 'Percentage')[['Student Name', 'Percentage', 'Grade']].to_dict('records')
        report['students_needing_attention'] = bottom_performers
        
        exam_analysis = {}
        
        mark_columns = ['CT1', 'CT2', 'CT3', 'CT4']
        for col in mark_columns:
            if col in self.processed_data.columns:
                exam_analysis[col] = {
                    'average': self.processed_data[col].mean(),
                    'highest': self.processed_data[col].max(),
                    'lowest': self.processed_data[col].min(),
                    'students_with_zero': (self.processed_data[col] == 0).sum()
                }
        
        exam_analysis['Best_3_CT_Avg'] = {
            'average': self.processed_data['Best_3_CT_Avg'].mean(),
            'highest': self.processed_data['Best_3_CT_Avg'].max(),
            'lowest': self.processed_data['Best_3_CT_Avg'].min(),
            'students_with_zero': (self.processed_data['Best_3_CT_Avg'] == 0).sum()
        }
        
        exam_analysis['Mid-Term_Original'] = {
            'average': self.processed_data['Mid-Term'].mean(),
            'highest': self.processed_data['Mid-Term'].max(),
            'lowest': self.processed_data['Mid-Term'].min(),
            'students_with_zero': (self.processed_data['Mid-Term'] == 0).sum()
        }
        
        exam_analysis['Mid-Term'] = {
            'average': self.processed_data['Midterm_Scaled'].mean(),
            'highest': self.processed_data['Midterm_Scaled'].max(),
            'lowest': self.processed_data['Midterm_Scaled'].min(),
            'students_with_zero': (self.processed_data['Midterm_Scaled'] == 0).sum()
        }
        
        # Presentation and Attendance
        for col in ['Presentation', 'Attendance']:
            if col in self.processed_data.columns:
                exam_analysis[col] = {
                    'average': self.processed_data[col].mean(),
                    'highest': self.processed_data[col].max(),
                    'lowest': self.processed_data[col].min(),
                    'students_with_zero': (self.processed_data[col] == 0).sum()
                }
        
        report['exam_analysis'] = exam_analysis
        
        return report

    def save_report_to_file(self, filename=None):
        """Save the detailed report to a text file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"result_analysis_report_{timestamp}.txt"

        filepath = os.path.join(self.output_dir, filename)
        report = self.generate_detailed_report()
        
        with open(filepath, 'w') as f:
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
            f.write("EXAM-WISE ANALYSIS:\n")
            f.write("-"*40 + "\n")
            for subject, stats in report['exam_analysis'].items():
                f.write(f"\n{subject}:\n")
                f.write(f"  Average: {stats['average']:.2f}\n")
                f.write(f"  Highest: {stats['highest']:.2f}\n")
                f.write(f"  Lowest: {stats['lowest']:.2f}\n")
                f.write(f"  Absent/Zero marks: {stats['students_with_zero']} students\n")
            
            f.write("\n" + "="*80 + "\n")
            f.write(f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n")
        
        print(f"Report saved to: {filename}")
        return filepath

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
        for subject, stats in report['exam_analysis'].items():
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

    def generate_graphs(self):
        """Generate various graphs and charts for analysis"""
        if self.processed_data is None:
            self.categorize_students()
        
        report = self.generate_detailed_report()
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Set style for better-looking graphs
        plt.style.use('default')  # Using default style instead of seaborn
        
        # Generate all visualizations
        self._create_grade_distribution(report)
        self._create_performance_analysis()
        self._create_assessment_breakdown()
        self._create_attendance_analysis()
        self._create_comparative_analysis()
        self._create_grade_progression()
        self._create_exam_wise_analysis()
        return self.output_dir

    def _create_grade_distribution(self, report):
        """Create pie chart for grade distribution"""
        plt.figure(figsize=(10, 8))
        grades = list(report['grade_distribution'].keys())
        values = list(report['grade_distribution'].values())
        # colors = plt.cm.Pastel1(np.linspace(0, 1, len(grades)))
        plt.pie(values, labels=grades, autopct='%1.1f%%')
        plt.title('Grade Distribution', pad=20, fontsize=14)
        plt.savefig(os.path.join(self.output_dir, 'grade_distribution.png'), 
                   bbox_inches='tight', dpi=300)
        plt.close()

    def _create_exam_wise_analysis(self):
        """Create bar chart for exam-wise analysis with visible lowest marks"""
        plt.figure(figsize=(12, 6))
        exam_analysis = self.generate_detailed_report()['exam_analysis']

        exams = list(exam_analysis.keys())
        exams.remove('Mid-Term_Original')  # Exclude original mid-term for clarity
        averages = [exam_analysis[subj]['average'] for subj in exams]
        highest = [exam_analysis[subj]['highest'] for subj in exams]
        lowest = [exam_analysis[subj]['lowest'] for subj in exams]
        x = np.arange(len(exams))
        width = 0.25
        bars1 = plt.bar(x - width, averages, width, label='Average', color='#2196F3')
        bars2 = plt.bar(x, highest, width, label='Highest', color='#4CAF50')
        bars3 = plt.bar(x + width, lowest, width, label='Lowest', color='#FF9800')

        plt.xticks(x, exams)
        plt.title('Exam-wise Analysis', pad=20, fontsize=14)
        plt.xlabel('Exams')
        plt.ylabel('Marks')
        plt.legend()
        plt.ylim(-1, max(highest) + 2)  # Set y-axis lower limit to -1

        # Add value labels for lowest marks
        for bar in bars3:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height + 0.1, f'{height:.1f}',
                     ha='center', va='bottom', fontsize=9, color='#FF9800')
        for bar in bars1:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height + 0.1, f'{height:.1f}',
                     ha='center', va='bottom', fontsize=9, color='#2196F3')
        for bar in bars2:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height + 0.1, f'{height:.1f}',
                     ha='center', va='bottom', fontsize=9, color='#4CAF50')

        plt.savefig(os.path.join(self.output_dir, 'exam_analysis.png'),
                    bbox_inches='tight', dpi=300)
        plt.close()

    def _create_performance_analysis(self):
        """Create line graph for student performance distribution"""
        plt.figure(figsize=(12, 6))
        sorted_data = self.processed_data.sort_values('Percentage', ascending=False)
        plt.plot(range(len(sorted_data)), sorted_data['Percentage'], 
                'b-', linewidth=2, color='#2196F3')
        plt.fill_between(range(len(sorted_data)), sorted_data['Percentage'], 
                        alpha=0.3, color='#2196F3')
        plt.title('Overall Performance Distribution', pad=20, fontsize=14)
        plt.xlabel('Student Rank')
        plt.ylabel('Percentage')
        plt.grid(True, alpha=0.3)
        plt.savefig(os.path.join(self.output_dir, 'performance_distribution.png'), 
                   bbox_inches='tight', dpi=300)
        plt.close()

    def _create_assessment_breakdown(self):
        """Create box plot for assessment score distribution"""
        plt.figure(figsize=(12, 6))
        components = ['CT1', 'CT2', 'CT3', 'CT4', 'Mid-Term']
        box_data = [self.processed_data[comp] for comp in components]
        
        bp = plt.boxplot(box_data, labels=components, patch_artist=True)
        
        # Customize box plot colors
        for box in bp['boxes']:
            box.set(facecolor='#4CAF50', alpha=0.7)
        
        plt.title('Assessment Score Distribution', pad=20, fontsize=14)
        plt.ylabel('Marks')
        plt.grid(True, alpha=0.3)
        plt.savefig(os.path.join(self.output_dir, 'assessment_distribution.png'), 
                   bbox_inches='tight', dpi=300)
        plt.close()

    def _create_attendance_analysis(self):
        """Create scatter plot for attendance vs performance correlation"""
        plt.figure(figsize=(10, 6))
        plt.scatter(self.processed_data['Attendance'], 
                   self.processed_data['Percentage'],
                   alpha=0.6, c='#FF9800')
        
        plt.title('Attendance vs Overall Performance', pad=20, fontsize=14)
        plt.xlabel('Attendance Score')
        plt.ylabel('Overall Percentage')
        plt.grid(True, alpha=0.3)
        plt.savefig(os.path.join(self.output_dir, 'attendance_correlation.png'), 
                   bbox_inches='tight', dpi=300)
        plt.close()

    def _create_comparative_analysis(self):
        """Create stacked bar chart for component-wise score distribution"""
        plt.figure(figsize=(12, 6))
        components = ['Best_3_CT_Avg', 'Midterm_Scaled', 'Presentation', 'Attendance']
        colors = ['#2196F3', '#4CAF50', '#FFC107', '#FF5722']
        
        bottom = np.zeros(len(self.processed_data))
        for component, color in zip(components, colors):
            plt.bar(range(len(self.processed_data)), 
                   self.processed_data[component], 
                   bottom=bottom, 
                   label=component,
                   alpha=0.7,
                   color=color)
            bottom += self.processed_data[component]
        
        plt.title('Score Component Distribution', pad=20, fontsize=14)
        plt.xlabel('Student Index')
        plt.ylabel('Marks')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'component_distribution.png'), 
                   bbox_inches='tight', dpi=300)
        plt.close()

    def _create_grade_progression(self):
        """Create line chart showing grade progression across assessments"""
        plt.figure(figsize=(12, 6))
        assessments = ['CT1', 'CT2', 'CT3', 'CT4', 'Mid-Term']
        for _, student in self.processed_data.iterrows():
            scores = [student[assessment] for assessment in assessments]
            plt.plot(assessments, scores, alpha=0.3)
        
        plt.title('Grade Progression Across Assessments')
        plt.xlabel('Assessment Type')
        plt.ylabel('Scores')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'grade_progression.png'))
        plt.close()

    def _create_ct_performance_box(self):
        """Create box plot for CT performance distribution"""
        plt.figure(figsize=(10, 6))
        ct_data = [self.processed_data[f'CT{i}'] for i in range(1, 5)]
        plt.boxplot(ct_data, labels=[f'CT{i}' for i in range(1, 5)])
        plt.title('CT Performance Distribution')
        plt.ylabel('Scores')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'ct_performance_box.png'))
        plt.close()

    def _create_student_performance_line(self):
        """Create line chart of overall student performance"""
        plt.figure(figsize=(15, 6))
        sorted_data = self.processed_data.sort_values('Percentage', ascending=False)
        plt.plot(range(len(sorted_data)), sorted_data['Percentage'], marker='o')
        plt.title('Student Performance Distribution')
        plt.xlabel('Student Rank')
        plt.ylabel('Overall Percentage')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'student_performance_line.png'))
        plt.close()

    def _create_component_contribution_stacked(self):
        """Create stacked bar chart showing contribution of each component"""
        plt.figure(figsize=(12, 6))
        components = ['Best_3_CT_Avg', 'Midterm_Scaled', 'Presentation', 'Attendance']
        
        bottom = np.zeros(len(self.processed_data))
        for component in components:
            plt.bar(range(len(self.processed_data)), 
                   self.processed_data[component], 
                   bottom=bottom, 
                   label=component)
            bottom += self.processed_data[component]
        
        plt.title('Component-wise Score Distribution')
        plt.xlabel('Student Index')
        plt.ylabel('Scores')
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'component_contribution.png'))
        plt.close()

    def _create_top_bottom_comparison(self, report):
        """Create comparative bar chart for top and bottom performers"""
        plt.figure(figsize=(12, 6))
        
        # Get top and bottom 5 students
        top_5 = report['top_performers']
        bottom_5 = report['students_needing_attention']
        
        # Prepare data
        names = ([student['Student Name'] for student in top_5] + 
                [student['Student Name'] for student in bottom_5])
        scores = ([student['Percentage'] for student in top_5] + 
                 [student['Percentage'] for student in bottom_5])
        colors = ['green']*5 + ['red']*5
        
        # Create bar chart
        plt.bar(range(len(names)), scores, color=colors)
        plt.xticks(range(len(names)), names, rotation=45, ha='right')
        plt.title('Top 5 vs Bottom 5 Performers')
        plt.ylabel('Overall Percentage')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'top_bottom_comparison.png'))
        plt.close()