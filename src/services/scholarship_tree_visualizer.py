import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import pandas as pd
import os
from src.utils.helpers import get_output_dir
from src.services.scholarship_service import ScholarshipService

class ScholarshipTreeVisualizer:
    def __init__(self):
        self.scholarship_service = ScholarshipService()

    def create_decision_tree_visualization(self):
        """Create a visual decision tree for scholarship allocation"""
        fig, ax = plt.subplots(1, 1, figsize=(20, 14))  # Increased figure size
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')

        # Define colors for different scholarship amounts
        colors = {
            15000: '#2E8B57',  # Sea Green
            12000: '#4169E1',  # Royal Blue
            9000: '#FF8C00',   # Dark Orange
            6000: '#DC143C',   # Crimson
            0: '#808080'       # Gray
        }

        # Root node
        root_box = FancyBboxPatch((4, 9), 2, 0.8,
                                 boxstyle="round,pad=0.1",
                                 facecolor='lightblue',
                                 edgecolor='black', linewidth=2)
        ax.add_patch(root_box)
        ax.text(5, 9.4, 'Scholarship\nEligibility', ha='center', va='center', fontsize=16, fontweight='bold')  # Increased font size

        # First level - SGPA >= 3.9
        high_sgpa_box = FancyBboxPatch((1, 7.5), 2, 0.8,
                                      boxstyle="round,pad=0.1",
                                      facecolor=colors[15000],
                                      edgecolor='black', linewidth=2)
        ax.add_patch(high_sgpa_box)
        ax.text(2, 7.9, 'SGPA ≥ 3.9\n15,000 TK', ha='center', va='center', fontsize=14, fontweight='bold', color='white')  # Increased font size

        # Second level - SGPA >= 3.8
        med_high_sgpa_box = FancyBboxPatch((4, 7.5), 2, 0.8,
                                          boxstyle="round,pad=0.1",
                                          facecolor=colors[9000],
                                          edgecolor='black', linewidth=2)
        ax.add_patch(med_high_sgpa_box)
        ax.text(5, 7.9, 'SGPA ≥ 3.8\n9,000 TK', ha='center', va='center', fontsize=14, fontweight='bold', color='white')  # Increased font size

        # Third level - Income check branch
        income_check_box = FancyBboxPatch((7, 7.5), 2, 0.8,
                                         boxstyle="round,pad=0.1",
                                         facecolor='lightyellow',
                                         edgecolor='black', linewidth=2)
        ax.add_patch(income_check_box)
        ax.text(8, 7.9, 'Income Check\nRequired', ha='center', va='center', fontsize=14, fontweight='bold')  # Increased font size

        # Income branches
        # Low income + SGPA >= 3.75
        low_income_high_box = FancyBboxPatch((6, 5.5), 2, 0.8,
                                            boxstyle="round,pad=0.1",
                                            facecolor=colors[12000],
                                            edgecolor='black', linewidth=2)
        ax.add_patch(low_income_high_box)
        ax.text(7, 5.9, 'Income < 50K\n& SGPA ≥ 3.75\n12,000 TK', ha='center', va='center', fontsize=12, fontweight='bold', color='white')  # Increased font size

        # Low income + SGPA >= 3.5
        low_income_med_box = FancyBboxPatch((8.5, 5.5), 2, 0.8,
                                           boxstyle="round,pad=0.1",
                                           facecolor=colors[6000],
                                           edgecolor='black', linewidth=2)
        ax.add_patch(low_income_med_box)
        ax.text(9.5, 5.9, 'Income < 50K\n& SGPA ≥ 3.5\n6,000 TK', ha='center', va='center', fontsize=12, fontweight='bold', color='white')  # Increased font size

        # No scholarship
        no_scholarship_box = FancyBboxPatch((4, 3.5), 2, 0.8,
                                           boxstyle="round,pad=0.1",
                                           facecolor=colors[0],
                                           edgecolor='black', linewidth=2)
        ax.add_patch(no_scholarship_box)
        ax.text(5, 3.9, 'No Scholarship\n0 TK', ha='center', va='center', fontsize=14, fontweight='bold', color='white')  # Increased font size

        # Draw connections
        connections = [
            # From root to first level
            ((5, 9), (2, 8.3)),
            ((5, 9), (5, 8.3)),
            ((5, 9), (8, 8.3)),
            # From income check to income branches
            ((8, 7.5), (7, 6.3)),
            ((8, 7.5), (9.5, 6.3)),
            # To no scholarship
            ((8, 7.5), (5, 4.3)),
        ]

        for start, end in connections:
            ax.annotate('', xy=end, xytext=start,
                       arrowprops=dict(arrowstyle='->', lw=2, color='black'))

        # Add labels for decision paths
        ax.text(1.5, 8.7, 'Yes', ha='center', va='center', fontsize=12, fontweight='bold', color='green')  # Increased font size
        ax.text(4.5, 8.7, 'No, but ≥ 3.8', ha='center', va='center', fontsize=12, fontweight='bold', color='orange')  # Increased font size
        ax.text(7.5, 8.7, 'No, but < 3.8', ha='center', va='center', fontsize=12, fontweight='bold', color='red')  # Increased font size

        ax.text(6.5, 6.7, 'Low Income', ha='center', va='center', fontsize=11, fontweight='bold', color='blue')  # Increased font size
        ax.text(9, 6.7, 'Low Income', ha='center', va='center', fontsize=11, fontweight='bold', color='blue')  # Increased font size
        ax.text(6, 4.7, 'High Income\nor Low SGPA', ha='center', va='center', fontsize=11, fontweight='bold', color='red')  # Increased font size

        # Add title and legend
        ax.text(5, 9.8, 'Scholarship Decision Tree', ha='center', va='center', fontsize=20, fontweight='bold')  # Increased font size

        # Create legend
        legend_elements = [
            patches.Patch(color=colors[15000], label='15,000 TK (SGPA ≥ 3.9)'),
            patches.Patch(color=colors[12000], label='12,000 TK (Income < 50K & SGPA ≥ 3.75)'),
            patches.Patch(color=colors[9000], label='9,000 TK (SGPA ≥ 3.8)'),
            patches.Patch(color=colors[6000], label='6,000 TK (Income < 50K & SGPA ≥ 3.5)'),
            patches.Patch(color=colors[0], label='0 TK (No Scholarship)')
        ]
        ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0, 0.3), fontsize=12)  # Increased font size

        # Add notes
        ax.text(5, 1.5, 'Notes:\n• Income threshold: 50,000 TK/month\n• SGPA scale: 0.0 - 4.0\n• Budget constraints may limit actual allocations',
                ha='center', va='center', fontsize=12,  # Increased font size
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgray', alpha=0.8))

        plt.tight_layout()

        # Save the visualization
        output_path = os.path.join(get_output_dir(), 'scholarship_decision_tree.png')
        os.makedirs(get_output_dir(), exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        return output_path

    def create_scholarship_statistics_tree(self):
        """Create a statistical analysis tree of scholarship distribution"""
        # Load data and perform analysis
        data = self.scholarship_service.load_and_prepare_data()

        # Calculate statistics for each scholarship tier
        stats = {}
        for _, row in data.iterrows():
            amount = self.scholarship_service.determine_scholarship_amount(row['SGPA'], row['monthly_income'])
            if amount not in stats:
                stats[amount] = {'count': 0, 'students': [], 'avg_sgpa': 0, 'total_sgpa': 0}
            stats[amount]['count'] += 1
            stats[amount]['students'].append(row['Name'])
            stats[amount]['total_sgpa'] += row['SGPA']

        # Calculate averages
        for amount in stats:
            if stats[amount]['count'] > 0:
                stats[amount]['avg_sgpa'] = stats[amount]['total_sgpa'] / stats[amount]['count']

        # Create visualization
        fig, ax = plt.subplots(1, 1, figsize=(16, 12))  # Increased figure size
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')

        # Colors
        colors = {
            15000: '#2E8B57',  # Sea Green
            12000: '#4169E1',  # Royal Blue
            9000: '#FF8C00',   # Dark Orange
            6000: '#DC143C',   # Crimson
            0: '#808080'       # Gray
        }

        # Title
        ax.text(5, 9.5, 'Scholarship Distribution Statistics', ha='center', va='center',
                fontsize=20, fontweight='bold')  # Increased font size

        # Create nodes for each scholarship amount
        y_positions = [8, 7, 6, 5, 4]
        amounts = [15000, 12000, 9000, 6000, 0]

        for i, amount in enumerate(amounts):
            if amount in stats:
                count = stats[amount]['count']
                avg_sgpa = stats[amount]['avg_sgpa']

                # Create box
                box = FancyBboxPatch((2, y_positions[i]-0.3), 6, 0.6,
                                   boxstyle="round,pad=0.1",
                                   facecolor=colors[amount],
                                   edgecolor='black', linewidth=2)
                ax.add_patch(box)

                # Add text
                if amount == 0:
                    text = f'No Scholarship: {count} students\nAvg SGPA: {avg_sgpa:.2f}'
                else:
                    text = f'{amount:,} TK: {count} students\nAvg SGPA: {avg_sgpa:.2f}'

                text_color = 'white' if amount != 0 else 'black'
                ax.text(5, y_positions[i], text, ha='center', va='center',
                       fontsize=14, fontweight='bold', color=text_color)  # Increased font size

        # Add total statistics
        total_students = len(data)
        scholarship_recipients = sum(stats[amount]['count'] for amount in stats if amount > 0)
        total_budget_needed = sum(amount * stats[amount]['count'] for amount in stats if amount > 0)

        stats_text = f'Total Students: {total_students}\n'
        stats_text += f'Scholarship Recipients: {scholarship_recipients}\n'
        stats_text += f'Students without Scholarship: {stats.get(0, {}).get("count", 0)}\n'
        stats_text += f'Total Budget Needed: {total_budget_needed:,} TK'

        ax.text(5, 2, stats_text, ha='center', va='center', fontsize=14,  # Increased font size
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.8))

        plt.tight_layout()

        # Save the visualization
        output_path = os.path.join(get_output_dir(), 'scholarship_statistics_tree.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        return output_path, stats

    def create_comprehensive_analysis(self):
        """Create a comprehensive scholarship analysis with multiple visualizations"""
        # Create decision tree
        decision_tree_path = self.create_decision_tree_visualization()

        # Create statistics tree
        stats_tree_path, stats = self.create_scholarship_statistics_tree()

        # Define colors for different scholarship amounts
        colors = {
            15000: '#2E8B57',  # Sea Green
            12000: '#4169E1',  # Royal Blue
            9000: '#FF8C00',   # Dark Orange
            6000: '#DC143C',   # Crimson
            0: '#808080'       # Gray
        }

        # Create a combined flow chart
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 12))  # Increased figure size

        # Left side - Process Flow
        ax1.set_xlim(0, 10)
        ax1.set_ylim(0, 10)
        ax1.axis('off')
        ax1.set_title('Scholarship Allocation Process', fontsize=16, fontweight='bold', pad=20)  # Increased font size

        # Process steps
        steps = [
            'Load Student Data',
            'Check SGPA ≥ 3.9',
            'Check SGPA ≥ 3.8',
            'Check Income < 50K',
            'Check SGPA ≥ 3.75',
            'Check SGPA ≥ 3.5',
            'Allocate Amount'
        ]

        for i, step in enumerate(steps):
            y_pos = 9 - i * 1.2
            box = FancyBboxPatch((2, y_pos-0.3), 6, 0.6,
                               boxstyle="round,pad=0.1",
                               facecolor='lightblue',
                               edgecolor='black', linewidth=1)
            ax1.add_patch(box)
            ax1.text(5, y_pos, step, ha='center', va='center', fontsize=12, fontweight='bold')  # Increased font size

            if i < len(steps) - 1:
                ax1.annotate('', xy=(5, y_pos-0.6), xytext=(5, y_pos-0.3),
                           arrowprops=dict(arrowstyle='->', lw=2, color='black'))

        # Right side - Distribution Chart
        ax2.set_title('Scholarship Amount Distribution', fontsize=16, fontweight='bold', pad=20)  # Increased font size

        amounts = [amount for amount in stats.keys() if amount > 0]
        counts = [stats[amount]['count'] for amount in amounts]
        colors_list = [colors[amount] for amount in amounts]

        bars = ax2.bar([f'{amount:,} TK' for amount in amounts], counts, color=colors_list)
        ax2.set_ylabel('Number of Students', fontsize=14)  # Increased font size
        ax2.set_xlabel('Scholarship Amount', fontsize=14)  # Increased font size
        ax2.tick_params(axis='both', which='major', labelsize=12)  # Increased tick label size

        # Add value labels on bars
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{count}', ha='center', va='bottom', fontweight='bold', fontsize=12)  # Increased font size

        plt.tight_layout()

        # Save the comprehensive analysis
        comprehensive_path = os.path.join(get_output_dir(), 'scholarship_comprehensive_analysis.png')
        plt.savefig(comprehensive_path, dpi=300, bbox_inches='tight')
        plt.close()

        return {
            'decision_tree': decision_tree_path,
            'statistics_tree': stats_tree_path,
            'comprehensive_analysis': comprehensive_path,
            'statistics': stats
        }

def generate_scholarship_visualizations():
    """Main function to generate all scholarship visualizations"""
    visualizer = ScholarshipTreeVisualizer()
    results = visualizer.create_comprehensive_analysis()

    print("Scholarship Analysis Visualizations Generated:")
    print(f"1. Decision Tree: {results['decision_tree']}")
    print(f"2. Statistics Tree: {results['statistics_tree']}")
    print(f"3. Comprehensive Analysis: {results['comprehensive_analysis']}")

    return results

if __name__ == "__main__":
    generate_scholarship_visualizations()
