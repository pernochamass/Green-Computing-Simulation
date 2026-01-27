import tkinter as tk
from tkinter import messagebox
import psutil
import time
import threading
import collections
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
from datetime import datetime

# --- 1. SYSTEM CONFIGURATION ---
# These simulate the ACPI P-States based on your project theory.
P_STATES = {
    "P0": {"power": 45.0, "desc": "Turbo (Max Performance)"},
    "P1": {"power": 35.0, "desc": "High (Standard)"},
    "P2": {"power": 20.0, "desc": "Balanced (Medium)"},
    "P3": {"power": 10.0, "desc": "Power Saver (Low)"}
}

class GreenComputingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Group 40: Green Computing Power Manager")
        self.root.geometry("1100x750")
        self.root.configure(bg="#f0f0f0")
        
        # --- Data Storage for Graphs & Reporting ---
        self.max_points = 60 # Show last 60 seconds
        self.time_history = [] 
        self.load_history = collections.deque([0]*self.max_points, maxlen=self.max_points)
        self.power_history = collections.deque([0]*self.max_points, maxlen=self.max_points)
        self.full_log = [] # Stores all data for the CSV report
        
        # --- System State ---
        self.is_green_mode = True 
        self.total_energy_saved = 0.0
        self.running = True
        self.start_time = time.time()

        # --- Build the Interface ---
        self.create_gui()
        
        # --- Start Monitoring Thread ---
        # This runs the logic in the background so the GUI doesn't freeze
        self.monitor_thread = threading.Thread(target=self.system_loop, daemon=True)
        self.monitor_thread.start()

    def create_gui(self):
        # 1. Header Section
        header = tk.Frame(self.root, bg="#2c3e50", pady=15)
        header.pack(fill=tk.X)
        tk.Label(header, text="Green Computing Power Manager", font=("Segoe UI", 22, "bold"), fg="white", bg="#2c3e50").pack()
        tk.Label(header, text="Group 40 - Real-Time Hardware-in-Loop Monitor", font=("Segoe UI", 10), fg="#bdc3c7", bg="#2c3e50").pack()

        # 2. Control Panel (Buttons)
        control_frame = tk.Frame(self.root, bg="#f0f0f0", pady=15)
        control_frame.pack(fill=tk.X)
        
        self.btn_mode = tk.Button(control_frame, text="MODE: GREEN (ADAPTIVE)", font=("Arial", 12, "bold"), 
                                  bg="#27ae60", fg="white", width=30, height=2, command=self.toggle_mode)
        self.btn_mode.pack(side=tk.LEFT, padx=50)

        self.btn_report = tk.Button(control_frame, text="GENERATE REPORT", font=("Arial", 12, "bold"), 
                                    bg="#2980b9", fg="white", width=25, height=2, command=self.generate_report)
        self.btn_report.pack(side=tk.RIGHT, padx=50)

        # 3. Live Stats Grid
        stats_frame = tk.LabelFrame(self.root, text="System Metrics", font=("Arial", 12), bg="#ecf0f1", padx=10, pady=10)
        stats_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.lbl_cpu = self.make_stat_box(stats_frame, "CPU Load", "0%", 0, "#e74c3c")
        self.lbl_freq = self.make_stat_box(stats_frame, "Frequency", "0 GHz", 1, "#8e44ad")
        self.lbl_state = self.make_stat_box(stats_frame, "ACPI State", "P3", 2, "#d35400")
        self.lbl_power = self.make_stat_box(stats_frame, "Est. Power", "0 W", 3, "#27ae60")
        self.lbl_saved = self.make_stat_box(stats_frame, "Total Saved", "0.0 J", 4, "#16a085")

        # 4. Real-Time Graph
        self.fig = Figure(figsize=(8, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Power Consumption vs. Workload")
        self.ax.set_xlabel("Time (Seconds)")
        self.ax.set_ylabel("Metric Value")
        self.ax.grid(True, alpha=0.3)
        
        # Plot lines
        self.line_load, = self.ax.plot([], [], label="CPU Load (%)", color="#3498db", linewidth=1.5)
        self.line_power, = self.ax.plot([], [], label="Power Usage (W)", color="#2ecc71", linewidth=2.5)
        self.ax.legend(loc="upper left")
        self.ax.set_ylim(0, 100)
        self.ax.set_xlim(0, 60)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    def make_stat_box(self, parent, title, value, col, color_code):
        frame = tk.Frame(parent, bg="white", relief="ridge", borderwidth=1)
        frame.grid(row=0, column=col, padx=10, sticky="ew")
        parent.grid_columnconfigure(col, weight=1)
        
        tk.Label(frame, text=title, font=("Arial", 10), fg="#7f8c8d", bg="white").pack(pady=(5,0))
        lbl = tk.Label(frame, text=value, font=("Arial", 18, "bold"), fg=color_code, bg="white")
        lbl.pack(pady=(0,10))
        return lbl

    def toggle_mode(self):
        self.is_green_mode = not self.is_green_mode
        if self.is_green_mode:
            self.btn_mode.config(text="MODE: GREEN (ADAPTIVE)", bg="#27ae60")
        else:
            self.btn_mode.config(text="MODE: STANDARD (PERFORMANCE)", bg="#c0392b")

    # --- THE BRAIN: LOGIC & ALGORITHM ---
    def system_loop(self):
        while self.running:
            # A. SENSORS (Input)
            cpu = psutil.cpu_percent(interval=0.5)
            freq = psutil.cpu_freq().current / 1000 if psutil.cpu_freq() else 2.5
            
            # B. DECISION ENGINE (The Algorithm)
            if self.is_green_mode:
                # Intelligent Scaling
                if cpu > 75: state = "P0"
                elif cpu > 40: state = "P1"
                elif cpu > 15: state = "P2"
                else: state = "P3"
            else:
                # Dumb Standard Mode (Always High)
                state = "P0" if cpu > 10 else "P1"

            # C. POWER ESTIMATION MODEL
            power = P_STATES[state]["power"]
            # Add dynamic fluctuation based on load
            real_power = power + (power * (cpu / 200)) 
            
            # Calculate Savings (Theoretical)
            # Compare current choice against "Standard Mode" baseline
            std_power = P_STATES["P0" if cpu > 10 else "P1"]["power"]
            savings_now = (std_power - power) * 0.5 # 0.5s interval
            if self.is_green_mode and savings_now > 0:
                self.total_energy_saved += savings_now

            # D. LOGGING
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.full_log.append([timestamp, cpu, freq, state, real_power])
            self.load_history.append(cpu)
            self.power_history.append(real_power)

            # E. UPDATE GUI (Must be done via root.after)
            self.root.after(0, self.update_display, cpu, freq, state, real_power)

    def update_display(self, cpu, freq, state, power):
        self.lbl_cpu.config(text=f"{cpu}%")
        self.lbl_freq.config(text=f"{freq:.2f} GHz")
        self.lbl_state.config(text=state)
        self.lbl_power.config(text=f"{power:.1f} W")
        self.lbl_saved.config(text=f"{self.total_energy_saved:.2f} J")
        
        # Update Graph Lines
        self.line_load.set_data(range(len(self.load_history)), self.load_history)
        self.line_power.set_data(range(len(self.power_history)), self.power_history)
        self.canvas.draw()

    def generate_report(self):
        filename = "Group40_Energy_Report.csv"
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "CPU_Load", "Frequency_GHz", "ACPI_State", "Power_Watts"])
            writer.writerows(self.full_log)
        messagebox.showinfo("Report Generated", f"Detailed Energy Report saved to:\n{filename}")

# --- STARTUP ---
if __name__ == "__main__":
    root = tk.Tk()
    app = GreenComputingSystem(root)
    root.mainloop()