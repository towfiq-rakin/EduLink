import os
from tkinter import Toplevel, messagebox, ttk
import customtkinter as ctk
from src.services.scholarship_service import ScholarshipService
from src.services.scholarship_tree_visualizer import generate_scholarship_visualizations
from src.utils.helpers import get_output_dir
import pandas as pd
from PIL import Image, ImageTk
import tkinter as tk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class ScholarshipWindow:
    def __init__(self, master):
        self.master = master
        self.window = Toplevel(master)
        self.window.title("Scholarship Management")
        self.window.geometry("900x700")

        self.scholarship_service = ScholarshipService()

        # Train the model on initialization
        data = self.scholarship_service.load_and_prepare_data()
        X, y = self.scholarship_service.prepare_training_data(data)
        self.scholarship_service.train_model(X, y)

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

            # Generate comprehensive visualizations
            visualization_results = generate_scholarship_visualizations()

            # Display results
            self.display_results(results)

            # Add visualization buttons after processing
            self.add_visualization_buttons(visualization_results)

        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def show_tree_rules(self):
        """Display the decision tree rules in a new window"""
        rules_path = os.path.join(get_output_dir(), 'scholarship_tree_rules.txt')

        if not os.path.exists(rules_path):
            messagebox.showerror("Error", "Tree rules file not found!")
            return

        # Create new window for rules
        rules_window = Toplevel(self.window)
        rules_window.title("Scholarship Decision Tree Rules")
        rules_window.geometry("800x600")

        # Create text widget with scrollbar
        text_frame = ctk.CTkFrame(rules_window)
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)

        text_widget = tk.Text(text_frame, wrap="none", font=('Courier', 12))
        scrollbar_y = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        scrollbar_x = ttk.Scrollbar(text_frame, orient="horizontal", command=text_widget.xview)

        text_widget.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        # Pack everything
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        text_widget.pack(side="left", fill="both", expand=True)

        # Load and display the rules
        with open(rules_path, 'r') as f:
            rules_text = f.read()
        text_widget.insert("1.0", rules_text)
        text_widget.configure(state="disabled")  # Make read-only

    def add_visualization_buttons(self, visualization_results):
        """Add buttons to view different visualizations"""
        # Create visualization buttons frame
        if hasattr(self, 'viz_frame'):
            self.viz_frame.destroy()

        self.viz_frame = ctk.CTkFrame(self.main_frame)
        self.viz_frame.pack(pady=10, padx=10, fill="x")

        # Title for visualization section
        viz_title = ctk.CTkLabel(
            self.viz_frame,
            text="Scholarship Analysis Visualizations",
            font=('Century Gothic', 16, 'bold')
        )
        viz_title.pack(pady=10)

        # Button frame for horizontal layout
        button_frame = ctk.CTkFrame(self.viz_frame)
        button_frame.pack(pady=10, fill="x")

        # Decision Tree Button
        decision_tree_btn = ctk.CTkButton(
            button_frame,
            text="View Decision Tree",
            command=lambda: self.show_visualization(
                visualization_results['decision_tree'],
                "Scholarship Decision Tree"
            ),
            font=('Century Gothic', 12)
        )
        decision_tree_btn.pack(side="left", padx=5, expand=True, fill="x")

        # Statistics Tree Button
        stats_tree_btn = ctk.CTkButton(
            button_frame,
            text="View Statistics Tree",
            command=lambda: self.show_visualization(
                visualization_results['statistics_tree'],
                "Scholarship Statistics Tree"
            ),
            font=('Century Gothic', 12)
        )
        stats_tree_btn.pack(side="left", padx=5, expand=True, fill="x")

        # Comprehensive Analysis Button
        comprehensive_btn = ctk.CTkButton(
            button_frame,
            text="View Comprehensive Analysis",
            command=lambda: self.show_visualization(
                visualization_results['comprehensive_analysis'],
                "Comprehensive Scholarship Analysis"
            ),
            font=('Century Gothic', 12)
        )
        comprehensive_btn.pack(side="left", padx=5, expand=True, fill="x")

        # Add Rules Button
        rules_btn = ctk.CTkButton(
            button_frame,
            text="View Decision Rules",
            command=self.show_tree_rules,
            font=('Century Gothic', 12)
        )
        rules_btn.pack(side="left", padx=5, expand=True, fill="x")

    def show_visualization(self, image_path, title):
        """Display visualization image in a new window"""
        try:
            if not os.path.exists(image_path):
                messagebox.showerror("Error", f"Visualization file not found: {image_path}")
                return

            # Create new window for visualization
            viz_window = Toplevel(self.window)
            viz_window.title(title)
            viz_window.geometry("1200x800")
            viz_window.configure(bg='white')

            # Load and display image
            image = Image.open(image_path)

            # Calculate scaling to fit window while maintaining aspect ratio
            window_width, window_height = 1150, 750
            img_width, img_height = image.size

            # Calculate scale factor
            scale_x = window_width / img_width
            scale_y = window_height / img_height
            scale = min(scale_x, scale_y, 1.0)  # Don't scale up, only down

            # Resize image if needed
            if scale < 1.0:
                new_width = int(img_width * scale)
                new_height = int(img_height * scale)
                image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(image)

            # Create canvas for scrolling
            canvas = tk.Canvas(viz_window, bg='white')
            scrollbar_v = ttk.Scrollbar(viz_window, orient="vertical", command=canvas.yview)
            scrollbar_h = ttk.Scrollbar(viz_window, orient="horizontal", command=canvas.xview)

            canvas.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

            # Pack scrollbars and canvas
            scrollbar_v.pack(side="right", fill="y")
            scrollbar_h.pack(side="bottom", fill="x")
            canvas.pack(side="left", fill="both", expand=True)

            # Add image to canvas
            canvas.create_image(0, 0, anchor="nw", image=photo)
            canvas.configure(scrollregion=canvas.bbox("all"))

            # Keep a reference to prevent garbage collection
            canvas.image = photo

            # Add close button
            close_btn = tk.Button(
                viz_window,
                text="Close",
                command=viz_window.destroy,
                font=('Century Gothic', 12),
                bg='#1f538d',
                fg='white',
                relief='flat',
                padx=20,
                pady=5
            )
            close_btn.pack(side="bottom", pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to display visualization: {str(e)}")

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
