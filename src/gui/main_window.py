import customtkinter as ctk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import os
import sys

# Add the project root to the path for imports
project_root = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.insert(0, project_root)

from src.services.result_analyzer import ResultAnalyzer

class MainWindow:
    def __init__(self, master):
        self.master = master
        master.title("EduLink - Student Management App")
        master.geometry("500x400")
        
        # Set the appearance mode and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Main frame
        self.main_frame = ctk.CTkFrame(master)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title label
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="Welcome to EduLink!", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=30)

        # Subtitle
        self.subtitle_label = ctk.CTkLabel(
            self.main_frame,
            text="Student Management & Analysis System",
            font=ctk.CTkFont(size=16)
        )
        self.subtitle_label.pack(pady=10)

        # Buttons frame
        self.buttons_frame = ctk.CTkFrame(self.main_frame)
        self.buttons_frame.pack(pady=40)

        # Result Analysis button
        self.result_analysis_button = ctk.CTkButton(
            self.buttons_frame,
            text="📊 Result Analysis",
            command=self.open_result_window,
            width=200,
            height=50,
            font=ctk.CTkFont(size=16)
        )
        self.result_analysis_button.pack(pady=10)

        # Scholarship Management button
        self.scholarship_button = ctk.CTkButton(
            self.buttons_frame,
            text="🎓 Scholarship Analysis",
            command=self.open_scholarship_window,
            width=200,
            height=50,
            font=ctk.CTkFont(size=16)
        )
        self.scholarship_button.pack(pady=10)

        # Exit button
        self.exit_button = ctk.CTkButton(
            self.buttons_frame,
            text="❌ Exit",
            command=master.quit,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color="red",
            hover_color="darkred"
        )
        self.exit_button.pack(pady=20)

    def open_scholarship_window(self):
        """Open scholarship analysis window with result analyzer output"""
        scholarship_window = ScholarshipAnalysisWindow(self.master)

    def open_result_window(self):
        """Open result analysis window"""
        result_window = ResultAnalysisWindow(self.master)

class ScholarshipAnalysisWindow:
    def __init__(self, parent):
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Scholarship Analysis - Result Overview")
        self.window.geometry("900x700")
        
        # Main frame with scrollable content
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="🎓 Scholarship Eligibility Analysis",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=20)
        
        # Create scrollable frame for results
        self.scrollable_frame = ctk.CTkScrollableFrame(self.main_frame, width=850, height=500)
        self.scrollable_frame.pack(fill="both", expand=True, pady=10)
        
        # Load and analyze data button
        self.analyze_button = ctk.CTkButton(
            self.main_frame,
            text="📈 Generate Analysis Report",
            command=self.generate_analysis,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.analyze_button.pack(pady=10)
        
        # Close button
        self.close_button = ctk.CTkButton(
            self.main_frame,
            text="Close",
            command=self.window.destroy,
            width=100,
            height=30
        )
        self.close_button.pack(pady=5)
        
        # Auto-generate analysis on window open
        self.generate_analysis()
    
    def generate_analysis(self):
        """Generate comprehensive scholarship analysis"""
        try:
            # Clear previous content
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            
            # Load data from result.csv
            dataset_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'result.csv')
            analyzer = ResultAnalyzer(dataset_path)
            
            if analyzer.load_data():
                analyzer.preprocess_data()
                analyzer.calculate_total_and_percentage()
                analyzer.categorize_students()
                report = analyzer.generate_detailed_report()
                student_results = analyzer.get_student_results()
                
                # Display grading system info
                grading_info = ctk.CTkLabel(
                    self.scrollable_frame,
                    text="📋 GRADING SYSTEM\n" +
                         "• Mid-term: 20 marks (scaled from 40)\n" +
                         "• Best 3 CT Average: 10 marks\n" +
                         "• Presentation: 10 marks\n" +
                         "• Attendance: 10 marks\n" +
                         "• Total: 50 marks",
                    font=ctk.CTkFont(size=12),
                    justify="left"
                )
                grading_info.pack(pady=10, padx=10, anchor="w")
                
                # Basic statistics
                stats_text = f"📊 BASIC STATISTICS\n" \
                           f"Total Students: {report['total_students']}\n" \
                           f"Average Percentage: {report['average_percentage']:.2f}%\n" \
                           f"Highest Percentage: {report['highest_percentage']:.2f}%\n" \
                           f"Lowest Percentage: {report['lowest_percentage']:.2f}%"
                
                stats_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=stats_text,
                    font=ctk.CTkFont(size=12),
                    justify="left"
                )
                stats_label.pack(pady=10, padx=10, anchor="w")
                
                # Top performers (Scholarship candidates)
                top_performers_text = "🏆 TOP SCHOLARSHIP CANDIDATES (Top 10)\n"
                top_10 = student_results.nlargest(10, 'Percentage')
                for i, (_, student) in enumerate(top_10.iterrows(), 1):
                    top_performers_text += f"{i:2d}. {student['Student Name']} - {student['Percentage']:.2f}% (Grade: {student['Grade']})\n"
                
                top_performers_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=top_performers_text,
                    font=ctk.CTkFont(size=11),
                    justify="left"
                )
                top_performers_label.pack(pady=10, padx=10, anchor="w")
                
                # Category distribution
                category_text = "📈 PERFORMANCE CATEGORIES\n"
                for category, count in report['category_distribution'].items():
                    percentage = (count / report['total_students']) * 100
                    category_text += f"• {category}: {count} students ({percentage:.1f}%)\n"
                
                category_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=category_text,
                    font=ctk.CTkFont(size=12),
                    justify="left"
                )
                category_label.pack(pady=10, padx=10, anchor="w")
                
                # Scholarship eligibility criteria
                excellent_students = student_results[student_results['Category'] == 'Excellent']
                good_students = student_results[student_results['Category'] == 'Good']
                
                eligibility_text = f"🎓 SCHOLARSHIP ELIGIBILITY ANALYSIS\n" \
                                 f"• Excellent Students (≥80%): {len(excellent_students)} - Highly Recommended\n" \
                                 f"• Good Students (65-79%): {len(good_students)} - Recommended\n" \
                                 f"• Total Eligible: {len(excellent_students) + len(good_students)} students"
                
                eligibility_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=eligibility_text,
                    font=ctk.CTkFont(size=12, weight="bold"),
                    justify="left",
                    text_color="green"
                )
                eligibility_label.pack(pady=10, padx=10, anchor="w")
                
                # Students needing attention
                bottom_performers_text = "⚠️ STUDENTS NEEDING ATTENTION (Bottom 5)\n"
                for i, student in enumerate(report['students_needing_attention'], 1):
                    bottom_performers_text += f"{i}. {student['Student Name']} - {student['Percentage']:.2f}% (Grade: {student['Grade']})\n"
                
                attention_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=bottom_performers_text,
                    font=ctk.CTkFont(size=11),
                    justify="left",
                    text_color="orange"
                )
                attention_label.pack(pady=10, padx=10, anchor="w")
                
            else:
                error_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text="❌ Error: Could not load data from result.csv",
                    font=ctk.CTkFont(size=14),
                    text_color="red"
                )
                error_label.pack(pady=20)
                
        except Exception as e:
            error_label = ctk.CTkLabel(
                self.scrollable_frame,
                text=f"❌ Error generating analysis: {str(e)}",
                font=ctk.CTkFont(size=12),
                text_color="red"
            )
            error_label.pack(pady=20)

class ResultAnalysisWindow:
    def __init__(self, parent):
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Detailed Result Analysis")
        self.window.geometry("800x600")
        
        # Main frame
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            self.main_frame,
            text="📊 Detailed Result Analysis",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Text area for detailed report
        self.text_area = ctk.CTkTextbox(self.main_frame, width=750, height=450)
        self.text_area.pack(pady=10)
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(self.main_frame)
        buttons_frame.pack(pady=10)
        
        # Generate report button
        generate_button = ctk.CTkButton(
            buttons_frame,
            text="Generate Report",
            command=self.generate_detailed_report,
            width=120
        )
        generate_button.pack(side="left", padx=5)
        
        # Close button
        close_button = ctk.CTkButton(
            buttons_frame,
            text="Close",
            command=self.window.destroy,
            width=80
        )
        close_button.pack(side="right", padx=5)
        
        # Auto-generate report
        self.generate_detailed_report()
    
    def generate_detailed_report(self):
        """Generate and display detailed analysis report"""
        try:
            dataset_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'result.csv')
            analyzer = ResultAnalyzer(dataset_path)
            
            if analyzer.load_data():
                analyzer.preprocess_data()
                analyzer.calculate_total_and_percentage()
                analyzer.categorize_students()
                
                # Generate report text
                report_text = "="*80 + "\n"
                report_text += "EDULINK - DETAILED RESULT ANALYSIS REPORT\n"
                report_text += "="*80 + "\n\n"
                
                # Add all report sections
                report = analyzer.generate_detailed_report()
                student_results = analyzer.get_student_results()
                
                report_text += "GRADING SYSTEM:\n"
                report_text += "-"*40 + "\n"
                report_text += "• Mid-term: 20 marks (scaled from 40)\n"
                report_text += "• Best 3 CT Average: 10 marks\n"
                report_text += "• Presentation: 10 marks\n"
                report_text += "• Attendance: 10 marks\n"
                report_text += "• Total: 50 marks\n\n"
                
                report_text += "BASIC STATISTICS:\n"
                report_text += "-"*40 + "\n"
                report_text += f"Total Students: {report['total_students']}\n"
                report_text += f"Average Percentage: {report['average_percentage']:.2f}%\n"
                report_text += f"Highest Percentage: {report['highest_percentage']:.2f}%\n"
                report_text += f"Lowest Percentage: {report['lowest_percentage']:.2f}%\n"
                report_text += f"Median Percentage: {report['median_percentage']:.2f}%\n\n"
                
                # Add all other sections...
                report_text += "TOP 10 PERFORMERS:\n"
                report_text += "-"*40 + "\n"
                top_10 = student_results.nlargest(10, 'Percentage')
                for i, (_, student) in enumerate(top_10.iterrows(), 1):
                    report_text += f"{i:2d}. {student['Student Name']} - {student['Percentage']:.2f}% (Grade: {student['Grade']})\n"
                
                # Clear and insert new text
                self.text_area.delete("1.0", "end")
                self.text_area.insert("1.0", report_text)
                
            else:
                self.text_area.delete("1.0", "end")
                self.text_area.insert("1.0", "Error: Could not load data from result.csv")
                
        except Exception as e:
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", f"Error generating report: {str(e)}")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTk()
    main_window = MainWindow(root)
    root.mainloop()