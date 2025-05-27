from tkinter import Toplevel, Label, Entry, Button, messagebox
import customtkinter as ctk
from services.scholarship_service import ScholarshipService

class ScholarshipWindow:
    def __init__(self, master):
        self.master = master
        self.window = Toplevel(master)
        self.window.title("Scholarship Management")
        
        self.label = Label(self.window, text="Enter Student Details for Scholarship Recommendation")
        self.label.pack(pady=10)

        self.student_name_label = Label(self.window, text="Student Name:")
        self.student_name_label.pack(pady=5)
        self.student_name_entry = Entry(self.window)
        self.student_name_entry.pack(pady=5)

        self.student_grade_label = Label(self.window, text="Student Grade:")
        self.student_grade_label.pack(pady=5)
        self.student_grade_entry = Entry(self.window)
        self.student_grade_entry.pack(pady=5)

        self.submit_button = Button(self.window, text="Get Recommendation", command=self.get_recommendation)
        self.submit_button.pack(pady=20)

    def get_recommendation(self):
        name = self.student_name_entry.get()
        grade = self.student_grade_entry.get()

        if not name or not grade:
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return

        try:
            recommendation = ScholarshipService.get_recommendation(name, float(grade))
            messagebox.showinfo("Scholarship Recommendation", recommendation)
        except ValueError:
            messagebox.showerror("Input Error", "Grade must be a number.")
        except Exception as e:
            messagebox.showerror("Error", str(e))