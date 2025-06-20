import customtkinter as ctk
import os
import tkinter as tk
from PIL import Image, ImageTk
from src.services.result_analyzer import ResultAnalyzer
from src.services.cluster_analyzer import ClusterAnalyzer

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class TeachersMenu:
    def __init__(self, master):
        self.master = master
        master.title("BUP EduLink - Teachers Menu")
        master.geometry("1000x700")
        master.resizable(True, True)

        self.frame = ctk.CTkFrame(master=self.master, width=1000, height=700)
        self.frame.pack(fill="both", expand=True)

        self.label = ctk.CTkLabel(
            master=self.frame,
            text="Welcome to the Teachers Menu",
            font=('Century Gothic', 24, 'bold'),
        )
        self.label.pack(pady=20)

        # Create control panel
        self.control_panel = ctk.CTkFrame(self.frame)
        self.control_panel.pack(fill="x", padx=20, pady=10)
        
        # Add buttons to the control panel
        self.analyze_button = ctk.CTkButton(
            self.control_panel, 
            text="Analyze Results", 
            command=self.analyze_results,
            font=('Century Gothic', 14)
        )
        self.analyze_button.pack(side="left", padx=10, pady=10)
        
        self.cluster_button = ctk.CTkButton(
            self.control_panel,
            text="Cluster Analysis",
            command=self.perform_cluster_analysis,
            font=('Century Gothic', 14)
        )
        self.cluster_button.pack(side="left", padx=10, pady=10)

        self.view_reports_button = ctk.CTkButton(
            self.control_panel, 
            text="View Reports", 
            command=self.view_reports,
            font=('Century Gothic', 14)
        )
        self.view_reports_button.pack(side="left", padx=10, pady=10)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self.control_panel,
            text="",
            font=('Century Gothic', 12),
            text_color="#4CAF50"
        )
        self.status_label.pack(side="left", padx=20, pady=10)
        
        # Create scrollable frame for reports
        self.reports_container = ctk.CTkScrollableFrame(self.frame, width=950, height=550)
        self.reports_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Path to the result file
        self.dataset_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'result.csv')
        self.analyzer = ResultAnalyzer(self.dataset_path)
        self.cluster_analyzer = ClusterAnalyzer(self.dataset_path)

        # Check if data exists
        if not os.path.exists(self.dataset_path):
            self.status_label.configure(text="Error: Result file not found", text_color="#F44336")
    
    def analyze_results(self):
        """Analyze the results and generate graphs"""
        self.status_label.configure(text="Analyzing results...", text_color="#FFC107")
        self.master.update()
        
        # Load and process the data
        if self.analyzer.load_data():
            self.analyzer.preprocess_data()
            self.analyzer.calculate_total_and_percentage()
            self.analyzer.categorize_students()
            
            # Generate graphs
            output_dir = self.analyzer.generate_graphs()
            self.analyzer.save_report_to_file()
            self.status_label.configure(
                text=f"Analysis complete! Graphs saved to: {output_dir}", 
                text_color="#4CAF50"
            )
        else:
            self.status_label.configure(
                text="Error: Could not load data from file", 
                text_color="#F44336"
            )

    def perform_cluster_analysis(self):
        """Perform cluster analysis on the results"""
        self.status_label.configure(text="Performing cluster analysis...", text_color="#FFC107")
        self.master.update()

        # Run the full cluster analysis
        results = self.cluster_analyzer.run_full_analysis(n_clusters=3)

        if results['success']:
            self.status_label.configure(
                text="Cluster analysis complete! View the results in Reports.",
                text_color="#4CAF50"
            )

            # Show the cluster visualization immediately
            self.display_cluster_results(results)
        else:
            self.status_label.configure(
                text="Error: Could not complete cluster analysis",
                text_color="#F44336"
            )

    def display_cluster_results(self, results):
        """Display the cluster analysis results"""
        # Clear previous content
        for widget in self.reports_container.winfo_children():
            widget.destroy()

        # Create header
        header = ctk.CTkLabel(
            self.reports_container,
            text="Student Performance Clustering Results",
            font=('Century Gothic', 18, 'bold')
        )
        header.pack(pady=15)

        # Create container for cluster visualization
        viz_frame = ctk.CTkFrame(self.reports_container)
        viz_frame.pack(fill="x", pady=10, padx=10)

        # Display cluster visualization
        if results['cluster_plot']:
            self.display_image(viz_frame, results['cluster_plot'], max_height=400)

        # Create container for statistics
        stats_frame = ctk.CTkFrame(self.reports_container)
        stats_frame.pack(fill="x", pady=10, padx=10)

        # Display statistics for each group
        if results['statistics']:
            stats_header = ctk.CTkLabel(
                stats_frame,
                text="Group Statistics",
                font=('Century Gothic', 16, 'bold')
            )
            stats_header.pack(pady=10)

            for group, stats in results['statistics'].items():
                group_frame = ctk.CTkFrame(stats_frame)
                group_frame.pack(fill="x", pady=5, padx=10)

                group_label = ctk.CTkLabel(
                    group_frame,
                    text=f"{group} Group ({stats['count']} students)",
                    font=('Century Gothic', 14, 'bold')
                )
                group_label.pack(pady=5)

                stats_text = (
                    f"Average Score: {stats['avg_score']:.2f} | "
                    f"Range: {stats['min_score']:.2f} - {stats['max_score']:.2f}"
                )
                stats_label = ctk.CTkLabel(
                    group_frame,
                    text=stats_text,
                    font=('Century Gothic', 12)
                )
                stats_label.pack(pady=5)

                # Show top students in this group
                if stats['students']:
                    student_text = "Top Students: " + ", ".join(
                        [f"{s['name']} ({s['total']:.1f})" for s in stats['students'][:5]]
                    )
                    student_label = ctk.CTkLabel(
                        group_frame,
                        text=student_text,
                        font=('Century Gothic', 12),
                        wraplength=800
                    )
                    student_label.pack(pady=5, padx=10)

        # Add buttons to view full reports
        buttons_frame = ctk.CTkFrame(self.reports_container)
        buttons_frame.pack(fill="x", pady=10, padx=10)

        if results['report_file']:
            report_button = ctk.CTkButton(
                buttons_frame,
                text="View Full Report",
                command=lambda: self.open_file_externally(results['report_file']),
                font=('Century Gothic', 12)
            )
            report_button.pack(side="left", padx=10, pady=10)

        if results['csv_file']:
            csv_button = ctk.CTkButton(
                buttons_frame,
                text="View CSV Data",
                command=lambda: self.open_file_externally(results['csv_file']),
                font=('Century Gothic', 12)
            )
            csv_button.pack(side="left", padx=10, pady=10)

    def view_reports(self):
        """View the generated reports and graphs"""
        # Clear previous content
        for widget in self.reports_container.winfo_children():
            widget.destroy()
        
        # Check if output directory exists
        output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'output')
        if not os.path.exists(output_dir):
            label = ctk.CTkLabel(self.reports_container, text="No reports found. Generate analysis first.", font=('Century Gothic', 14))
            label.pack(pady=20)
            return
        
        # Get all PNG files in the output directory
        png_files = [f for f in os.listdir(output_dir) if f.endswith('.png')]
        
        if not png_files:
            label = ctk.CTkLabel(self.reports_container, text="No graphs found. Generate analysis first.", font=('Century Gothic', 14))
            label.pack(pady=20)
            return
        
        # Create a frame for each image (2 per row)
        for i, png_file in enumerate(png_files):
            if i % 2 == 0:
                row_frame = ctk.CTkFrame(self.reports_container)
                row_frame.pack(fill="x", pady=10, padx=5)
            
            # Create frame for image with title
            img_frame = ctk.CTkFrame(row_frame)
            img_frame.pack(side="left", padx=5, fill="both", expand=True)
            
            # Add title
            title = png_file.replace('.png', '').replace('_', ' ').title()
            title_label = ctk.CTkLabel(img_frame, text=title, font=('Century Gothic', 12, 'bold'))
            title_label.pack(pady=5)
            
            # Load and display the image
            img_path = os.path.join(output_dir, png_file)
            self.display_image(img_frame, img_path, max_height=280)
    
    def display_image(self, parent_frame, img_path, max_height=280):
        """Display an image in the given frame with a maximum height"""
        try:
            # Open the image and resize it
            img = Image.open(img_path)
            
            # Calculate new dimensions while maintaining aspect ratio
            width, height = img.size
            ratio = width / height
            new_height = min(max_height, height)
            new_width = int(new_height * ratio)
            
            # Resize image
            img = img.resize((new_width, new_height), Image.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(img)
            
            # Create label and display image
            img_label = tk.Label(parent_frame, image=photo, bg="#2b2b2b")
            img_label.image = photo  # Keep a reference to prevent garbage collection
            img_label.pack(pady=5)
            
            # Add "Open" button
            open_button = ctk.CTkButton(
                parent_frame, 
                text="View Full Size", 
                command=lambda p=img_path: self.open_image_externally(p),
                font=('Century Gothic', 12),
                width=100,
                height=25
            )
            open_button.pack(pady=5)
            
        except Exception as e:
            error_label = ctk.CTkLabel(parent_frame, text=f"Error loading image: {e}", text_color="#F44336")
            error_label.pack(pady=10)
    
    def open_image_externally(self, img_path):
        """Open the image in the default image viewer"""
        import subprocess
        import platform
        
        try:
            if platform.system() == 'Windows':
                os.startfile(img_path)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.call(['open', img_path])
            else:  # Linux
                subprocess.call(['xdg-open', img_path])
        except Exception as e:
            print(f"Error opening image externally: {e}")

    def open_file_externally(self, file_path):
        """Open a file with the default application"""
        import subprocess
        import platform

        try:
            if platform.system() == 'Windows':
                os.startfile(file_path)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.call(['open', file_path])
            else:  # Linux
                subprocess.call(['xdg-open', file_path])
        except Exception as e:
            print(f"Error opening file: {e}")
