import os
import sys
import customtkinter as ctk
from PIL import Image

# Set light mode for consistency
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.services.result_analyzer import ResultAnalyzer
from src.services.cluster_analyzer import ClusterAnalyzer
from src.services.scholarship_service import ScholarshipService
from src.gui.scholarship_window import ScholarshipWindow

class TeachersMenu:
    def __init__(self, master):
        self.master = master
        self.master.title("BUP EduLink - Teachers Dashboard")
        self.master.geometry("1280x800")
        self.master.resizable(True, True)
        self.master.minsize(1024, 768)

        # Initialize services
        self.data_file = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'result.csv')
        self.result_analyzer = ResultAnalyzer(data_file=self.data_file)
        self.cluster_analyzer = ClusterAnalyzer(data_file=self.data_file)
        self.scholarship_service = ScholarshipService()

        # Create main grid layout
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

        # Create sidebar
        self.create_sidebar()

        # Create main content area
        self.create_main_content()

        # Create dashboard widgets
        self.create_dashboard()

        # Initialize status bar
        self.create_status_bar()

    def create_sidebar(self):
        # Sidebar container
        self.sidebar = ctk.CTkFrame(self.master, width=250)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(10, 5), pady=10)
        self.sidebar.grid_rowconfigure(4, weight=1)  # Push version info to bottom
        self.sidebar.grid_propagate(False)

        # App logo/name
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        app_name = ctk.CTkLabel(
            logo_frame,
            text="BUP EduLink",
            font=('Century Gothic', 24, 'bold')
        )
        app_name.pack(pady=10)

        # Navigation menu
        menu_items = [
            ("Dashboard", self.show_dashboard),
            ("Analysis", self.show_analysis_view),
            ("Scholarships", self.show_scholarship_view),
            ("Reports", self.show_reports_view)
        ]

        for i, (text, command) in enumerate(menu_items, start=1):
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=command,
                height=40,
                font=('Century Gothic', 14)
            )
            btn.grid(row=i, column=0, padx=20, pady=5, sticky="ew")

        # Version info at bottom
        version_label = ctk.CTkLabel(
            self.sidebar,
            text="Version 1.0.0",
            font=('Century Gothic', 12)
        )
        version_label.grid(row=5, column=0, padx=20, pady=20, sticky="s")

    def create_main_content(self):
        # Main content container with tabs
        self.main_content = ctk.CTkFrame(self.master)
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        self.main_content.grid_rowconfigure(1, weight=1)
        self.main_content.grid_columnconfigure(0, weight=1)

        # Header
        self.header = ctk.CTkLabel(
            self.main_content,
            text="Welcome to Teachers Dashboard",
            font=('Century Gothic', 24, 'bold')
        )
        self.header.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="nw")

        # Content area
        self.content_frame = ctk.CTkFrame(self.main_content)
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(10, 20))
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

    def create_dashboard(self):
        # Clear existing content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Create grid layout for dashboard cards
        self.content_frame.grid_columnconfigure((0, 1), weight=1)
        self.content_frame.grid_rowconfigure((0, 1), weight=1)

        # Quick Stats Card
        stats_card = self.create_card(
            self.content_frame,
            "Quick Statistics",
            "View class performance metrics",
            0, 0
        )

        # Analysis Card
        analysis_card = self.create_card(
            self.content_frame,
            "Result Analysis",
            "Analyze student performance",
            0, 1
        )

        # Scholarship Card
        scholarship_card = self.create_card(
            self.content_frame,
            "Scholarship Management",
            "Manage student scholarships",
            1, 0
        )

        # Reports Card
        reports_card = self.create_card(
            self.content_frame,
            "Generated Reports",
            "Access all generated reports",
            1, 1
        )

    def create_card(self, parent, title, description, row, column):
        card = ctk.CTkFrame(parent)
        card.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=('Century Gothic', 16, 'bold')
        )
        title_label.pack(pady=(15, 5), padx=15)

        desc_label = ctk.CTkLabel(
            card,
            text=description,
            font=('Century Gothic', 12)
        )
        desc_label.pack(pady=(0, 15), padx=15)

        return card

    def create_status_bar(self):
        self.status_frame = ctk.CTkFrame(self.master, height=30)
        self.status_frame.grid(row=1, column=1, sticky="ew", padx=(5, 10), pady=(0, 10))
        self.status_frame.grid_propagate(False)

        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Ready",
            font=('Century Gothic', 12)
        )
        self.status_label.pack(side="left", padx=15)

    def show_dashboard(self):
        self.header.configure(text="Dashboard")
        self.create_dashboard()

    def show_analysis_view(self):
        self.header.configure(text="Analysis Center")
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Create analysis options
        options_frame = ctk.CTkFrame(self.content_frame)
        options_frame.pack(fill="x", padx=20, pady=20)

        analyze_btn = ctk.CTkButton(
            options_frame,
            text="Analyze Results",
            command=self.analyze_results,
            width=200,
            font=('Century Gothic', 14)
        )
        analyze_btn.pack(side="left", padx=10)

        cluster_btn = ctk.CTkButton(
            options_frame,
            text="Cluster Analysis",
            command=self.perform_cluster_analysis,
            width=200,
            font=('Century Gothic', 14)
        )
        cluster_btn.pack(side="left", padx=10)

        # Create results area
        self.results_area = ctk.CTkScrollableFrame(self.content_frame)
        self.results_area.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def show_scholarship_view(self):
        """Open the dedicated scholarship management window"""
        try:
            scholarship_window = ScholarshipWindow(self.master)
            self.status_label.configure(text="Scholarship window opened")
        except Exception as e:
            self.status_label.configure(text=f"Error opening scholarship window: {str(e)}")

    def show_reports_view(self):
        self.header.configure(text="Generated Reports")
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        reports_area = ctk.CTkScrollableFrame(self.content_frame)
        reports_area.pack(fill="both", expand=True, padx=20, pady=20)

        output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'output')
        if not os.path.exists(output_dir):
            ctk.CTkLabel(
                reports_area,
                text="No reports found. Generate analysis first.",
                font=('Century Gothic', 14)
            ).pack(pady=20)
            return

        # Find all PNG files in the output directory
        png_files = [f for f in os.listdir(output_dir) if f.lower().endswith('.png')]

        if not png_files:
            ctk.CTkLabel(
                reports_area,
                text="No graph reports found. Generate analysis first.",
                font=('Century Gothic', 14)
            ).pack(pady=20)
            return

        # Create a 2-column grid layout for the images
        reports_area.grid_columnconfigure(0, weight=1)
        reports_area.grid_columnconfigure(1, weight=1)

        # Load and display images in 2 columns
        for i, filename in enumerate(png_files):
            row = i // 2
            col = i % 2

            # Create a frame for each image and its info
            img_frame = ctk.CTkFrame(reports_area)
            img_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            # Add title
            title = filename.replace('.png', '').replace('_', ' ').title()
            ctk.CTkLabel(
                img_frame,
                text=title,
                font=('Century Gothic', 12, 'bold')
            ).pack(pady=(10, 5))

            # Load and resize the image
            img_path = os.path.join(output_dir, filename)
            try:
                img = Image.open(img_path)
                # Resize while maintaining aspect ratio
                img.thumbnail((300, 200))
                ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(300, 200))

                # Display the image
                img_label = ctk.CTkLabel(img_frame, image=ctk_img, text="")
                img_label.pack(pady=5)
                img_label.image = ctk_img  # Keep a reference to prevent garbage collection

                # Add a view button
                view_btn = ctk.CTkButton(
                    img_frame,
                    text="View Full Size",
                    command=lambda f=img_path: self.open_file_externally(f),
                    width=120,
                    font=('Century Gothic', 12)
                )
                view_btn.pack(pady=(5, 10))
            except Exception as e:
                error_label = ctk.CTkLabel(img_frame, text=f"Error loading image: {e}")
                error_label.pack(pady=10)

    def analyze_results(self):
        """Analyze student results"""
        try:
            # Clear content and create loading indicator
            for widget in self.results_area.winfo_children():
                widget.destroy()

            # Create loading indicator
            loading_frame = ctk.CTkFrame(self.results_area)
            loading_frame.pack(fill="both", expand=True)

            loading_label = ctk.CTkLabel(
                loading_frame,
                text="Analyzing student results...",
                font=('Century Gothic', 18)
            )
            loading_label.pack(pady=(100, 20))

            progress = ctk.CTkProgressBar(loading_frame, width=300)
            progress.pack(pady=10)
            progress.start()

            self.status_label.configure(text="Analyzing results...")

            # Update UI before proceeding
            self.master.update()

            # Load and process data
            if not self.result_analyzer.load_data():
                raise Exception("Failed to load data")

            # Process data and properly handle presentation marks
            self.result_analyzer.preprocess_data()
            results = self.result_analyzer.calculate_total_and_percentage()
            self.result_analyzer.categorize_students()

            # Check if presentation data is present in the original data
            if 'Presentation' in results.columns:
                print(f"Presentation data found. Sample values: {results['Presentation'].head()}")
            elif 'presentation' in results.columns:
                print(f"Lowercase presentation column found, mapping to Presentation")
                results['Presentation'] = results['presentation']
            else:
                print("Warning: No presentation column found. Adding default values.")
                # If no presentation data is found, add a message to the UI
                self.status_label.configure(text="Warning: Presentation data missing. Using default values.")

            # Force recalculation of total with presentation included
            results['Total_Obtained'] = (
                results['Midterm_Scaled'] +  # 20 marks
                results['Best_3_CT_Avg'] +   # 10 marks
                results['Presentation'] +    # 10 marks
                results['Attendance']        # 10 marks
            )

            results['Percentage'] = (results['Total_Obtained'] / 50) * 100

            # Debug output to verify presentation data is included
            print(f"First 5 rows of processed data:")
            print(results[['Student Name', 'Best_3_CT_Avg', 'Midterm_Scaled', 'Presentation', 'Attendance', 'Total_Obtained']].head())

            # Update the processed data with correct values
            self.result_analyzer.processed_data = results

            # Generate graphs and report
            self.result_analyzer.generate_graphs()
            self.result_analyzer.save_report_to_file()

            # Clear loading frame
            loading_frame.destroy()

            # Display header
            header = ctk.CTkLabel(
                self.results_area,
                text="Results Analysis",
                font=('Century Gothic', 24, 'bold')
            )
            header.pack(pady=20)

            # Add button to view full text report
            report_btn_frame = ctk.CTkFrame(self.results_area, fg_color="transparent")
            report_btn_frame.pack(fill="x", pady=(0, 20), padx=20)

            view_report_btn = ctk.CTkButton(
                report_btn_frame,
                text="View Full Text Report",
                command=self.show_text_report,
                font=('Century Gothic', 14),
                fg_color="#4CAF50",
                hover_color="#388E3C",
                width=200
            )
            view_report_btn.pack(pady=10)

            # Display visualizations - Updated to show all generated graphs
            viz_paths = {
                'Grade Distribution': 'grade_distribution.png',
                'Component Distribution': 'component_distribution.png',
                'Basic Statistics': 'basic_statistics.png',
                'Exam Analysis': 'exam_analysis.png',
                'Top vs Bottom Student': 'top_bottom_comparison.png'
            }

            output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'output')

            for title, filename in viz_paths.items():
                img_path = os.path.join(output_dir, filename)
                if os.path.exists(img_path):
                    section_frame = ctk.CTkFrame(self.results_area)
                    section_frame.pack(fill="x", pady=(20, 30), padx=20)

                    title_label = ctk.CTkLabel(
                        section_frame,
                        text=title,
                        font=('Century Gothic', 18, 'bold')
                    )
                    title_label.pack(pady=(20, 10))

                    self.display_image(section_frame, img_path, max_height=500)

            self.status_label.configure(text="Analysis complete! Check the graphs above.")

        except Exception as e:
            self.status_label.configure(text=f"Error during analysis: {str(e)}")

    def perform_cluster_analysis(self):
        """Perform cluster analysis on the results"""
        try:
            # Clear content and create loading indicator
            for widget in self.results_area.winfo_children():
                widget.destroy()

            # Create loading indicator
            loading_frame = ctk.CTkFrame(self.results_area)
            loading_frame.pack(fill="both", expand=True)

            loading_label = ctk.CTkLabel(
                loading_frame,
                text="Performing cluster analysis...",
                font=('Century Gothic', 18)
            )
            loading_label.pack(pady=(100, 20))

            progress = ctk.CTkProgressBar(loading_frame, width=300)
            progress.pack(pady=10)
            progress.start()

            self.status_label.configure(text="Performing cluster analysis...")

            # Update UI before proceeding
            self.master.update()

            # Perform clustering
            results = self.cluster_analyzer.run_full_analysis()

            # Clear loading frame
            loading_frame.destroy()

            # Display results with enhanced header
            header_frame = ctk.CTkFrame(self.results_area)
            header_frame.pack(fill="x", padx=20, pady=(20, 30))

            header = ctk.CTkLabel(
                header_frame,
                text="Student Performance Clusters",
                font=('Century Gothic', 20, 'bold')
            )
            header.pack(pady=15)

            # Display cluster visualization
            output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'output')
            cluster_plot = os.path.join(output_dir, "student_clusters.png")

            if os.path.exists(cluster_plot):
                viz_frame = ctk.CTkFrame(self.results_area)
                viz_frame.pack(fill="x", pady=10, padx=10)
                self.display_image(viz_frame, cluster_plot)

                # Display report info as well
                report_path = os.path.join(output_dir, "cluster_analysis_report.txt")
                if os.path.exists(report_path):
                    report_frame = ctk.CTkFrame(self.results_area)
                    report_frame.pack(fill="x", pady=20, padx=20)

                    report_header = ctk.CTkLabel(
                        report_frame,
                        text="Cluster Analysis Report",
                        font=('Century Gothic', 18, 'bold')
                    )
                    report_header.pack(pady=(15, 10))

                    report_btn = ctk.CTkButton(
                        report_frame,
                        text="View Full Report",
                        command=lambda: self.open_file_externally(report_path),
                        width=150,
                        font=('Century Gothic', 14)
                    )
                    report_btn.pack(pady=10)
            else:
                error_label = ctk.CTkLabel(
                    self.results_area,
                    text="Cluster visualization not found. Try running the analysis again.",
                    font=('Century Gothic', 14)
                )
                error_label.pack(pady=20)

            self.status_label.configure(text="Cluster analysis complete!")

        except Exception as e:
            self.status_label.configure(text=f"Error during cluster analysis: {str(e)}")

    def _get_latest_file(self, directory, prefix):
        """Get the most recent file with given prefix from directory"""
        files = [f for f in os.listdir(directory) if f.startswith(prefix)]
        if not files:
            return None
        return os.path.join(directory, max(files))

    def clear_content(self):
        """Clear the scholarship results frame"""
        if hasattr(self, 'scholarship_results_frame'):
            for widget in self.scholarship_results_frame.winfo_children():
                widget.destroy()

    def display_image(self, parent_frame, img_path, max_height=500):
        """Display an image in the given frame with a maximum height"""
        try:
            img = Image.open(img_path)
            width, height = img.size
            ratio = width / height
            new_height = min(max_height, height)
            new_width = int(new_height * ratio)
            max_width = 900
            if new_width > max_width:
                new_width = max_width
                new_height = int(new_width / ratio)
            resample_method = getattr(Image, 'Resampling', Image).LANCZOS
            img = img.resize((new_width, new_height), resample_method)
            from customtkinter import CTkImage
            ctk_img = CTkImage(light_image=img, size=(new_width, new_height))
            label = ctk.CTkLabel(parent_frame, image=ctk_img, text="")
            label.pack(pady=20)
        except Exception as e:
            error_label = ctk.CTkLabel(parent_frame, text=f"Error loading image: {e}")
            error_label.pack(pady=10)

    def view_reports(self):
        """View the generated graphs"""
        try:
            self.clear_content()

            output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'output')
            if not os.path.exists(output_dir):
                self.status_label.configure(
                    text="No reports found. Generate analysis first."
                )
                return

            header = ctk.CTkLabel(
                self.scholarship_results_frame,
                text="Generated Graphs",
                font=('Century Gothic', 20, 'bold')
            )
            header.pack(pady=20)

            # Create scrollable frame for graphs
            graphs_frame = ctk.CTkScrollableFrame(self.scholarship_results_frame)
            graphs_frame.pack(fill="both", expand=True, padx=10, pady=10)

            # Get all graph files (PNG only)
            files = os.listdir(output_dir)
            graph_files = [(f, os.path.getmtime(os.path.join(output_dir, f)))
                      for f in files if f.endswith('.png')]
            graph_files.sort(key=lambda x: x[1], reverse=True)

            if not graph_files:
                no_graphs_label = ctk.CTkLabel(
                    graphs_frame,
                    text="No graphs found. Generate analysis first.",
                    font=('Century Gothic', 14)
                )
                no_graphs_label.pack(pady=20)
                return

            # Display each graph
            for filename, timestamp in graph_files:
                file_path = os.path.join(output_dir, filename)
                graph_frame = ctk.CTkFrame(graphs_frame)
                graph_frame.pack(fill="x", padx=5, pady=10, expand=True)

                # Add title based on filename
                title = filename.replace('_', ' ').replace('.png', '').title()
                title_label = ctk.CTkLabel(
                    graph_frame,
                    text=title,
                    font=('Century Gothic', 16, 'bold')
                )
                title_label.pack(pady=(10, 5))

                # Display graph thumbnail
                self.display_image(graph_frame, file_path, max_height=300)

                # Button frame for actions
                button_frame = ctk.CTkFrame(graph_frame)
                button_frame.pack(fill="x", padx=10, pady=5)

                # Full view button
                full_view_button = ctk.CTkButton(
                    button_frame,
                    text="Full View",
                    command=lambda f=file_path: self.show_full_image(f),
                    width=120,
                    font=('Century Gothic', 12)
                )
                full_view_button.pack(side="left", padx=10, pady=5)

                # Open externally button
                external_button = ctk.CTkButton(
                    button_frame,
                    text="Open Externally",
                    command=lambda f=file_path: self.open_image_externally(f),
                    width=120,
                    font=('Century Gothic', 12)
                )
                external_button.pack(side="right", padx=10, pady=5)

        except Exception as e:
            self.status_label.configure(
                text=f"Error loading graphs: {str(e)}"
            )

    def show_full_image(self, img_path):
        """Show image in a full view popup window"""
        try:
            # Create a new top-level window
            top = ctk.CTkToplevel(self.master)
            top.title("Full Image View")
            top.geometry("1000x800")
            top.grab_set()  # Make the window modal

            # Create a frame to hold the image
            frame = ctk.CTkFrame(top)
            frame.pack(fill="both", expand=True, padx=20, pady=20)

            # Display the image at larger size
            img = Image.open(img_path)

            # Calculate new dimensions while maintaining aspect ratio
            max_width, max_height = 900, 700
            width, height = img.size
            ratio = width / height

            if width > max_width:
                width = max_width
                height = int(width / ratio)

            if height > max_height:
                height = max_height
                width = int(height * ratio)

            # Resize image
            resample_method = getattr(Image, 'Resampling', Image).LANCZOS
            img = img.resize((width, height), resample_method)

            # Convert to CTkImage and display
            from customtkinter import CTkImage
            ctk_img = CTkImage(light_image=img, size=(width, height))
            label = ctk.CTkLabel(frame, image=ctk_img, text="")
            label.pack(expand=True)

            # Add a close button
            close_button = ctk.CTkButton(
                top,
                text="Close",
                command=top.destroy,
                width=100,
                font=('Century Gothic', 12)
            )
            close_button.pack(pady=10)

        except Exception as e:
            print(f"Error showing full image: {e}")

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
        try:
            if os.name == 'nt':  # Windows
                os.startfile(file_path)
            elif os.name == 'posix':  # Linux/Mac
                if os.system('which xdg-open') == 0:  # Linux
                    os.system(f'xdg-open "{file_path}"')
                else:  # macOS
                    os.system(f'open "{file_path}"')
        except Exception as e:
            self.status_label.configure(
                text=f"Error opening file: {str(e)}"
            )

    def show_scholarship_manager(self):
        """Show scholarship management interface"""
        # Clear previous content
        for widget in self.scholarship_results_frame.winfo_children():
            widget.destroy()

        # Create header
        header = ctk.CTkLabel(
            self.scholarship_results_frame,
            text="Scholarship Management",
            font=('Century Gothic', 20, 'bold')
        )
        header.pack(pady=20)

        # Create budget input frame
        budget_frame = ctk.CTkFrame(self.scholarship_results_frame)
        budget_frame.pack(pady=20)

        budget_label = ctk.CTkLabel(
            budget_frame,
            text="Total Scholarship Budget (TK):",
            font=('Century Gothic', 14)
        )
        budget_label.pack(side="left", padx=5)

        self.budget_entry = ctk.CTkEntry(budget_frame, width=200)
        self.budget_entry.pack(side="left", padx=5)

        process_button = ctk.CTkButton(
            budget_frame,
            text="Process Scholarships",
            command=self.process_scholarships,
            font=('Century Gothic', 14)
        )
        process_button.pack(side="left", padx=20)

        # Create scrollable results frame
        self.scholarship_results_frame = ctk.CTkScrollableFrame(
            self.scholarship_results_frame,
            height=400
        )
        self.scholarship_results_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Add instructions
        intro_label = ctk.CTkLabel(
            self.scholarship_results_frame,
            text="Enter the total scholarship budget and click Process to distribute scholarships.",
            font=('Century Gothic', 12),
            wraplength=600
        )
        intro_label.pack(pady=10)

    def process_scholarships(self):
        """Process scholarship distribution"""
        try:
            budget = float(self.budget_entry.get())
            if budget <= 0:
                self.status_label.configure(
                    text="Error: Budget must be greater than 0!"
                )
                return

            # Clear previous results
            for widget in self.scholarship_results_frame.winfo_children():
                widget.destroy()

            # Show processing indicator
            processing_frame = ctk.CTkFrame(self.scholarship_results_frame, fg_color="transparent")
            processing_frame.pack(fill="both", expand=True)

            processing_label = ctk.CTkLabel(
                processing_frame,
                text="Processing scholarship distribution...",
                font=('Century Gothic', 16)
            )
            processing_label.pack(pady=(50, 20))

            progress = ctk.CTkProgressBar(processing_frame, width=300)
            progress.pack(pady=10)
            progress.start()

            self.status_label.configure(
                text="Processing scholarships..."
            )

            # Update UI before continuing
            self.master.update()

            # Process scholarships
            results = self.scholarship_service.allocate_scholarships(budget)

            # Stop progress indicator
            progress.stop()
            processing_frame.destroy()

            # Display results
            self.display_scholarship_results(results)

            self.status_label.configure(
                text="Scholarship distribution completed successfully!"
            )

        except ValueError:
            self.status_label.configure(
                text="Error: Please enter a valid number for the budget."
            )
        except Exception as e:
            self.status_label.configure(
                text=f"Error: {str(e)}"
            )

    def _darken_color(self, hex_color, factor=0.8):
        """Darken a hex color by multiplying RGB values by factor"""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        r = max(0, min(255, int(r * factor)))
        g = max(0, min(255, int(g * factor)))
        b = max(0, min(255, int(b * factor)))
        return f"#{r:02x}{g:02x}{b:02x}"

    def display_scholarship_results(self, results):
        """Display scholarship distribution results"""
        # Clear previous results
        for widget in self.scholarship_results_frame.winfo_children():
            widget.destroy()

        # Display summary statistics
        if not results.empty:
            total_recipients = len(results[results['scholarship_amount'] > 0])
            total_awarded = results['scholarship_amount'].sum()

            summary = ctk.CTkLabel(
                self.scholarship_results_frame,
                text=f"""
                Scholarship Distribution Summary
                
                Total Recipients: {total_recipients}
                Total Amount Awarded: {total_awarded:,.2f} TK
                Average Award: {(total_awarded/total_recipients if total_recipients > 0 else 0):,.2f} TK
                """,
                font=('Century Gothic', 14),
                justify="left"
            )
            summary.pack(pady=20)

            # Display visualization if available
            viz_path = os.path.join(os.path.dirname(__file__), '..', '..', 'output', 'scholarship_distribution.png')
            if os.path.exists(viz_path):
                self.display_image(self.scholarship_results_frame, viz_path, max_height=300)

            # Add export buttons
            export_frame = ctk.CTkFrame(self.scholarship_results_frame, fg_color="transparent")
            export_frame.pack(pady=(15, 5), fill="x")

            export_label = ctk.CTkLabel(
                export_frame,
                text="Export Results:",
                font=('Century Gothic', 14, 'bold')
            )
            export_label.pack(side="left", padx=10)

            export_csv_btn = ctk.CTkButton(
                export_frame,
                text="Export to CSV",
                command=lambda: self.export_scholarship_results(results, 'csv'),
                font=('Century Gothic', 12),
                width=120,
                height=32
            )
            export_csv_btn.pack(side="left", padx=10)

            export_excel_btn = ctk.CTkButton(
                export_frame,
                text="Export to Excel",
                command=lambda: self.export_scholarship_results(results, 'excel'),
                font=('Century Gothic', 12),
                width=120,
                height=32
            )
            export_excel_btn.pack(side="left", padx=10)

            # Create table headers
            headers_frame = ctk.CTkFrame(self.scholarship_results_frame, corner_radius=8)
            headers_frame.pack(fill="x", padx=5, pady=(15, 5))

            headers = ['Student ID', 'Name', 'SGPA', 'Scholarship Amount (TK)']
            for header in headers:
                label = ctk.CTkLabel(
                    headers_frame,
                    text=header,
                    font=('Century Gothic', 13, 'bold')
                )
                label.pack(side="left", expand=True, padx=5, pady=8)

            # Check if there are any scholarship recipients
            if 'scholarship_amount' in results.columns:
                recipients = results[results['scholarship_amount'] > 0].sort_values('scholarship_amount', ascending=False)

                if not recipients.empty:
                    # Create container for rows
                    rows_container = ctk.CTkScrollableFrame(
                        self.scholarship_results_frame,
                        height=400,
                        corner_radius=8,
                        fg_color="transparent"
                    )
                    rows_container.pack(fill="x", expand=True, padx=5, pady=5)

                    # Display recipients with alternating row colors
                    for i, (_, row) in enumerate(recipients.iterrows()):
                        # Use alternating colors for better readability
                        bg_color = "#2B2B2B" if i % 2 == 0 else "#333333"

                        row_frame = ctk.CTkFrame(rows_container, corner_radius=4, fg_color=bg_color)
                        row_frame.pack(fill="x", padx=5, pady=2)

                        ctk.CTkLabel(
                            row_frame,
                            text=str(row['student_id']),
                            font=('Century Gothic', 13)
                        ).pack(side="left", expand=True, padx=5, pady=8)

                        ctk.CTkLabel(
                            row_frame,
                            text=row['name'],
                            font=('Century Gothic', 13)
                        ).pack(side="left", expand=True, padx=5, pady=8)

                        # Format SGPA display without colors
                        sgpa_value = row['sgpa']
                        ctk.CTkLabel(
                            row_frame,
                            text=f"{sgpa_value:.2f}",
                            font=('Century Gothic', 13, 'bold')
                        ).pack(side="left", expand=True, padx=5, pady=8)

                        ctk.CTkLabel(
                            row_frame,
                            text=f"{row['scholarship_amount']:,.0f} TK",
                            font=('Century Gothic', 13, 'bold')
                        ).pack(side="left", expand=True, padx=5, pady=8)
                else:
                    # No recipients despite having data
                    no_recipients_label = ctk.CTkLabel(
                        self.scholarship_results_frame,
                        text="No students qualified for scholarships with the given budget.",
                        font=('Century Gothic', 14)
                    )
                    no_recipients_label.pack(pady=20)
            else:
                # Missing scholarship amount column
                no_data_label = ctk.CTkLabel(
                    self.scholarship_results_frame,
                    text="No scholarship data available. Processing may have failed.",
                    font=('Century Gothic', 14)
                )
                no_data_label.pack(pady=20)
        else:
            no_data_label = ctk.CTkLabel(
                self.scholarship_results_frame,
                text="No scholarship data available.",
                font=('Century Gothic', 14)
            )
            no_data_label.pack(pady=20)

    def export_scholarship_results(self, results, format_type):
        """Export scholarship results to CSV or Excel"""
        try:
            if results.empty:
                self.status_label.configure(text="No data to export")
                return
            output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'output')
            os.makedirs(output_dir, exist_ok=True)
            recipients = results[results['scholarship_amount'] > 0].sort_values('scholarship_amount', ascending=False)
            if format_type.lower() == 'csv':
                file_path = os.path.join(output_dir, 'scholarship_recipients.csv')
                recipients.to_csv(file_path, index=False)
                file_type = 'CSV'
            elif format_type.lower() == 'excel':
                file_path = os.path.join(output_dir, 'scholarship_recipients.xlsx')
                recipients.to_excel(file_path, index=False)
                file_type = 'Excel'
            else:
                raise ValueError(f"Unsupported export format: {format_type}")
            self.status_label.configure(text=f"Scholarship data exported to {file_type} file successfully: {os.path.basename(file_path)}")
            open_file_window = ctk.CTkToplevel(self.master)
            open_file_window.title("Export Complete")
            open_file_window.geometry("400x150")
            open_file_window.resizable(False, False)
            open_file_window.lift()
            open_file_window.attributes("-topmost", True)
            message = ctk.CTkLabel(open_file_window, text=f"Scholarship data has been exported to {file_type} format.\nWould you like to open the file?", font=('Century Gothic', 12), wraplength=350)
            message.pack(pady=(20, 15))
            button_frame = ctk.CTkFrame(open_file_window, fg_color="transparent")
            button_frame.pack(pady=10)
            open_btn = ctk.CTkButton(button_frame, text="Open File", command=lambda: [self.open_file_externally(file_path), open_file_window.destroy()], font=('Century Gothic', 12), width=100)
            open_btn.pack(side="left", padx=10)
            close_btn = ctk.CTkButton(
                button_frame,
                text="Close",
                command=open_file_window.destroy,
                font=('Century Gothic', 12),
                width=100
            )
            close_btn.pack(side="left", padx=10)
        except Exception as e:
            self.status_label.configure(text=f"Error exporting data: {str(e)}")

    def show_text_report(self):
        """Display the full text report in a new window"""
        try:
            # Generate the report if it doesn't exist yet
            output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'output')
            report_path = os.path.join(output_dir, "result_analysis_report.txt")

            # If report doesn't exist, generate it
            if not os.path.exists(report_path):
                self.result_analyzer.save_report_to_file()

            # Create a new toplevel window
            report_window = ctk.CTkToplevel(self.master)
            report_window.title("Full Result Analysis Report")
            report_window.geometry("900x700")
            report_window.grab_set()  # Make the window modal

            # Create a frame for the report content
            frame = ctk.CTkFrame(report_window)
            frame.pack(fill="both", expand=True, padx=20, pady=20)

            # Add a header
            header = ctk.CTkLabel(
                frame,
                text="Complete Result Analysis Report",
                font=('Century Gothic', 20, 'bold')
            )
            header.pack(pady=(10, 20))

            # Create a scrollable text widget to display the report
            text_container = ctk.CTkScrollableFrame(frame)
            text_container.pack(fill="both", expand=True, padx=10, pady=10)

            # Read the report file
            with open(report_path, 'r') as f:
                report_text = f.read()

            # Display the report in a text widget with monospaced font
            text_widget = ctk.CTkTextbox(text_container, width=800, height=500, font=("Courier New", 12))
            text_widget.pack(fill="both", expand=True, padx=5, pady=5)
            text_widget.insert("1.0", report_text)
            text_widget.configure(state="disabled")  # Make it read-only

            # Add buttons at the bottom
            button_frame = ctk.CTkFrame(report_window, fg_color="transparent")
            button_frame.pack(pady=15)

            # Open in external app button
            open_btn = ctk.CTkButton(
                button_frame,
                text="Open in External App",
                command=lambda: self.open_file_externally(report_path),
                width=150,
                font=('Century Gothic', 12)
            )
            open_btn.pack(side="left", padx=10)

            # Copy to clipboard button
            copy_btn = ctk.CTkButton(
                button_frame,
                text="Copy to Clipboard",
                command=lambda: self.copy_to_clipboard(report_text),
                width=150,
                font=('Century Gothic', 12)
            )
            copy_btn.pack(side="left", padx=10)

            # Close button
            close_btn = ctk.CTkButton(
                button_frame,
                text="Close",
                command=report_window.destroy,
                width=100,
                font=('Century Gothic', 12)
            )
            close_btn.pack(side="left", padx=10)

        except Exception as e:
            self.status_label.configure(text=f"Error showing report: {str(e)}")

    def copy_to_clipboard(self, text):
        """Copy text to clipboard"""
        try:
            self.master.clipboard_clear()
            self.master.clipboard_append(text)
            self.status_label.configure(text="Report copied to clipboard successfully!")
        except Exception as e:
            self.status_label.configure(text=f"Error copying to clipboard: {str(e)}")
