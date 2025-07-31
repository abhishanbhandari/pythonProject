import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class CSVAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced CSV Analyzer")
        self.root.geometry("700x550")
        self.data = None

        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)

        tk.Button(top_frame, text="Load CSV", command=self.load_csv, font=("Arial", 10, "bold"), bg="#add8e6").pack(side=tk.LEFT, padx=10)

        self.col_label = tk.Label(self.root, text="Select Column:", font=("Arial", 10))
        self.col_label.pack()

        self.column_combo = ttk.Combobox(self.root, width=50, state="readonly")
        self.column_combo.pack(pady=5)

        chart_frame = tk.Frame(self.root)
        chart_frame.pack(pady=10)

        tk.Button(chart_frame, text="Bar Chart", width=12, command=self.bar_chart, bg="#90ee90").pack(side=tk.LEFT, padx=5)
        tk.Button(chart_frame, text="Pie Chart", width=12, command=self.pie_chart, bg="#ffcccb").pack(side=tk.LEFT, padx=5)
        tk.Button(chart_frame, text="Histogram", width=12, command=self.histogram, bg="#ffffcc").pack(side=tk.LEFT, padx=5)

        tk.Button(self.root, text="Show Statistics", command=self.show_stats, font=("Arial", 10), bg="#d3d3d3").pack(pady=10)

        info_frame = tk.Frame(self.root)
        info_frame.pack(pady=5)

        self.col_count_label = tk.Label(info_frame, text="Total Columns: N/A", font=("Arial", 10, "bold"), fg="navy")
        self.col_count_label.pack()

        self.column_list_text = tk.Text(info_frame, height=5, width=70)
        self.column_list_text.pack(pady=5)
        self.column_list_text.insert(tk.END, "Column names will appear here.")
        self.column_list_text.config(state='disabled')

        self.status = tk.Label(self.root, text="Load a CSV file to begin", fg="blue")
        self.status.pack()

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                self.data = pd.read_csv(file_path)
                self.column_combo['values'] = list(self.data.columns)
                self.status.config(text=f"Loaded: {file_path.split('/')[-1]}")

                # Update column count and list
                self.col_count_label.config(text=f"Total Columns: {self.data.shape[1]}")
                self.column_list_text.config(state='normal')
                self.column_list_text.delete("1.0", tk.END)
                self.column_list_text.insert(tk.END, "\n".join(self.data.columns.tolist()))
                self.column_list_text.config(state='disabled')

            except Exception as e:
                messagebox.showerror("Error", f"Failed to load CSV:\n{str(e)}")

    def get_selected_column(self):
        col = self.column_combo.get()
        if not col or col not in self.data.columns:
            messagebox.showwarning("Select Column", "Please select a valid column.")
            return None
        return col

    def bar_chart(self):
        col = self.get_selected_column()
        if col:
            counts = self.data[col].value_counts()
            counts.plot(kind="bar", color="skyblue")
            plt.title(f"Bar Chart - {col}")
            plt.xlabel(col)
            plt.ylabel("Count")
            plt.tight_layout()
            plt.show()

    def pie_chart(self):
        col = self.get_selected_column()
        if col:
            counts = self.data[col].value_counts().nlargest(5)
            counts.plot(kind="pie", autopct='%1.1f%%')
            plt.title(f"Top 5 Values - {col}")
            plt.ylabel("")
            plt.tight_layout()
            plt.show()

    def histogram(self):
        col = self.get_selected_column()
        if col and np.issubdtype(self.data[col].dtype, np.number):
            self.data[col].dropna().plot(kind="hist", bins=10, color="orange", edgecolor="black")
            plt.title(f"Histogram - {col}")
            plt.xlabel(col)
            plt.ylabel("Frequency")
            plt.tight_layout()
            plt.show()
        else:
            messagebox.showinfo("Invalid", "Select a numeric column for histogram.")

    def show_stats(self):
        if self.data is not None:
            stats = self.data.describe(include="all").transpose()
            stat_window = tk.Toplevel(self.root)
            stat_window.title("Summary Statistics")

            text = tk.Text(stat_window, wrap="none", width=100, height=30)
            text.insert(tk.END, stats.to_string())
            text.pack()
        else:
            messagebox.showinfo("No Data", "Please load a CSV first.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVAnalyzer(root)
    root.mainloop()
