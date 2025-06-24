import os
from tkinter import Toplevel, messagebox, ttk
import customtkinter as ctk
from src.services.scholarship_service import ScholarshipService
import pandas as pd

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ScholarshipWindow:
    def __init__(self, master):
        self.master = master
        self.window = Toplevel(master)
        self.window.title("Scholarship Management")
        self.window.geometry("800x600")

        self.scholarship_service = ScholarshipService()

        # Main container frame
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.pack(fill="both", expand=True)

        # Budget Input Frame
        self.budget_frame = ctk.CTkFrame(self.main_frame)
        self.budget_frame.pack(pady=20, padx=10, fill="x")

        self.budget_label = ctk.CTkLabel(
            self.budget_frame,
            text="Total Scholarship Budget (TK):",
            font=('Century Gothic', 14)
        )
        self.budget_label.pack(side="left", padx=5)

        self.budget_entry = ctk.CTkEntry(self.budget_frame)
        self.budget_entry.pack(side="right", padx=5, expand=True, fill="x")

        # Process Button
        self.process_button = ctk.CTkButton(
            self.main_frame,
            text="Process Scholarships",
            command=self.process_scholarships,
            font=('Century Gothic', 14)
        )
        self.process_button.pack(pady=20)

        # Results container and table setup
        self.results_container = ctk.CTkFrame(self.main_frame)
        self.results_container.pack(fill="both", expand=True, padx=10, pady=10)
        # Summary label
        self.results_label = ctk.CTkLabel(
            self.results_container,
            text="Enter budget and click Process to distribute scholarships",
            font=('Century Gothic', 12),
            justify="left"
        )
        self.results_label.pack(anchor="w", pady=(0,10))
        # Table frame for Treeview
        self.table_frame = ctk.CTkFrame(self.results_container)
        self.table_frame.pack(fill="both", expand=True)
        # Create Treeview
        columns = ("student_id", "name", "sgpa", "scholarship_amount")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        # Define headings
        self.tree.heading("student_id", text="Student ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("sgpa", text="SGPA")
        self.tree.heading("scholarship_amount", text="Scholarship Amount")
        # Define column widths and alignment
        self.tree.column("student_id", anchor="w", width=100)
        self.tree.column("name", anchor="w", width=200)
        self.tree.column("sgpa", anchor="w", width=80)
        self.tree.column("scholarship_amount", anchor="w", width=150)
        # Add scrollbar
        self.tree_scroll = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.tree_scroll.set)
        # Pack tree and scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        self.tree_scroll.pack(side="right", fill="y")

    def process_scholarships(self):
        try:
            budget = float(self.budget_entry.get())
            if budget <= 0:
                messagebox.showerror("Error", "Budget must be greater than 0!")
                return

            # Process scholarships
            results = self.scholarship_service.allocate_scholarships(budget)

            # Generate visualization
            output_path = self.scholarship_service.visualize_distribution(results)

            # Display results
            self.display_results(results)

        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def display_results(self, results):
        # Display summary statistics
        recipients = results[results['scholarship_amount'] > 0]
        total_recipients = len(recipients)
        total_awarded = recipients['scholarship_amount'].sum()

        summary = f"""
        Scholarship Distribution Complete!
        
        Total Recipients: {total_recipients}
        Total Amount Awarded: {total_awarded:,.2f} TK
        Average Award: {(total_awarded/total_recipients if total_recipients > 0 else 0):,.2f} TK
        
        Distribution visualization saved in output directory
        """

        # Update summary label
        self.results_label.configure(text=summary)

        # Clear existing rows in tree
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Insert new rows
        for _, row in recipients.sort_values('scholarship_amount', ascending=False).iterrows():
            self.tree.insert("", "end", values=(
                row['student_id'],
                row['name'],
                f"{row['sgpa']:.2f}",
                f"{row['scholarship_amount']:,.0f} TK"
            ))
