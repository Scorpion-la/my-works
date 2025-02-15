#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      ADITYA
#
# Created:     15/02/2025
# Copyright:   (c) ADITYA 2025
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk, messagebox
import time
from datetime import datetime
import pytz

class ClockApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Modern Clock App")
        self.window.geometry("800x600")

        style = ttk.Style()
        style.theme_use('clam')

        style.configure('Tab', padding=[20, 10], font=('Helvetica', 12))
        style.configure('TButton', padding=10, font=('Helvetica', 10))
        style.configure('Clock.TLabel', font=('Helvetica', 48, 'bold'), foreground='#2c3e50')
        style.configure('Title.TLabel', font=('Helvetica', 14), foreground='#7f8c8d')

        self.main_container = ttk.Frame(self.window, padding="20")
        self.main_container.pack(expand=True, fill='both')

        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(expand=True, fill='both')

        self.clock_tab = ttk.Frame(self.notebook)
        self.stopwatch_tab = ttk.Frame(self.notebook)
        self.timer_tab = ttk.Frame(self.notebook)
        self.world_time_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.clock_tab, text='Clock')
        self.notebook.add(self.stopwatch_tab, text='Stopwatch')
        self.notebook.add(self.timer_tab, text='Timer')
        self.notebook.add(self.world_time_tab, text='World Time')

        self.setup_clock()
        self.setup_stopwatch()
        self.setup_timer()
        self.setup_world_time()

        self.update_clock()

    def setup_clock(self):
        clock_container = ttk.Frame(self.clock_tab, padding="20")
        clock_container.pack(expand=True, fill='both')

        ttk.Label(clock_container, text="Current Time", style='Title.TLabel').pack(pady=(0, 10))
        self.clock_label = ttk.Label(clock_container, style='Clock.TLabel')
        self.clock_label.pack(pady=20)
        self.date_label = ttk.Label(clock_container, font=('Helvetica', 16))
        self.date_label.pack(pady=10)

    def setup_stopwatch(self):
        stopwatch_container = ttk.Frame(self.stopwatch_tab, padding="20")
        stopwatch_container.pack(expand=True, fill='both')

        ttk.Label(stopwatch_container, text="Stopwatch", style='Title.TLabel').pack(pady=(0, 20))

        self.stopwatch_label = ttk.Label(stopwatch_container, font=('Helvetica', 48, 'bold'), text="00:00:00")
        self.stopwatch_label.pack(pady=20)

        btn_frame = ttk.Frame(stopwatch_container)
        btn_frame.pack(pady=20)

        self.stopwatch_running = False
        self.stopwatch_time = 0

        ttk.Button(btn_frame, text="Start", command=self.start_stopwatch).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Stop", command=self.stop_stopwatch).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Reset", command=self.reset_stopwatch).pack(side=tk.LEFT, padx=10)

    def setup_timer(self):
        timer_container = ttk.Frame(self.timer_tab, padding="20")
        timer_container.pack(expand=True, fill='both')

        ttk.Label(timer_container, text="Timer", style='Title.TLabel').pack(pady=(0, 20))

        input_frame = ttk.Frame(timer_container)
        input_frame.pack(pady=20)

        self.hours_var = tk.StringVar(value="00")
        self.minutes_var = tk.StringVar(value="00")
        self.seconds_var = tk.StringVar(value="00")

        spinbox_style = {'width': 3, 'font': ('Helvetica', 16), 'wrap': True}

        ttk.Spinbox(input_frame, from_=0, to=23, textvariable=self.hours_var, **spinbox_style).pack(side=tk.LEFT)
        ttk.Label(input_frame, text=":", font=('Helvetica', 16)).pack(side=tk.LEFT, padx=5)
        ttk.Spinbox(input_frame, from_=0, to=59, textvariable=self.minutes_var, **spinbox_style).pack(side=tk.LEFT)
        ttk.Label(input_frame, text=":", font=('Helvetica', 16)).pack(side=tk.LEFT, padx=5)
        ttk.Spinbox(input_frame, from_=0, to=59, textvariable=self.seconds_var, **spinbox_style).pack(side=tk.LEFT)

        self.timer_label = ttk.Label(timer_container, font=('Helvetica', 48, 'bold'))
        self.timer_label.pack(pady=20)

        self.timer_running = False
        self.timer_remaining = 0

        btn_frame = ttk.Frame(timer_container)
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="Start", command=self.start_timer).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Stop", command=self.stop_timer).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Reset", command=self.reset_timer).pack(side=tk.LEFT, padx=10)

    def setup_world_time(self):
        world_container = ttk.Frame(self.world_time_tab, padding="20")
        world_container.pack(expand=True, fill='both')

        ttk.Label(world_container, text="World Time", style='Title.TLabel').pack(pady=(0, 20))

        timezones = [
            ('US/Pacific', 'San Francisco'),
            ('US/Eastern', 'New York'),
            ('Europe/London', 'London'),
            ('Asia/Tokyo', 'Tokyo'),
            ('Australia/Sydney', 'Sydney')
        ]

        for tz, city_label in timezones:
            frame = ttk.Frame(world_container)
            frame.pack(pady=10)

            ttk.Label(frame, text=f"{city_label}:", font=('Helvetica', 14)).pack(side=tk.LEFT, padx=(0, 20))

            label = ttk.Label(frame, font=('Helvetica', 14, 'bold'))
            label.pack(side=tk.LEFT)
            setattr(self, f'label_{city_label.lower().replace(" ", "_")}', label)

    def start_stopwatch(self):
        self.stopwatch_running = True

    def stop_stopwatch(self):
        self.stopwatch_running = False

    def reset_stopwatch(self):
        self.stopwatch_running = False
        self.stopwatch_time = 0
        self.stopwatch_label.config(text="00:00:00")

    def start_timer(self):
        try:
            hours = int(self.hours_var.get())
            minutes = int(self.minutes_var.get())
            seconds = int(self.seconds_var.get())
            total_seconds = hours * 3600 + minutes * 60 + seconds
            if total_seconds <= 0:
                raise ValueError("Time must be positive")
            self.timer_remaining = total_seconds
            self.timer_running = True
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for hours, minutes, and seconds.")

    def stop_timer(self):
        self.timer_running = False

    def reset_timer(self):
        self.timer_running = False
        self.hours_var.set("00")
        self.minutes_var.set("00")
        self.seconds_var.set("00")
        self.timer_remaining = 0
        self.timer_label.config(text="00:00:00")

    def update_clock(self):
        current_time = time.strftime('%H:%M:%S')
        current_date = time.strftime('%A, %B %d, %Y')
        self.clock_label.config(text=current_time)
        self.date_label.config(text=current_date)

        timezones = [
            ('US/Pacific', 'San Francisco'),
            ('US/Eastern', 'New York'),
            ('Europe/London', 'London'),
            ('Asia/Tokyo', 'Tokyo'),
            ('Australia/Sydney', 'Sydney')
        ]

        for tz_name, city_label in timezones:
            try:
                tz = pytz.timezone(tz_name)
                local_time = datetime.now(tz).strftime('%H:%M:%S')
                getattr(self, f'label_{city_label.lower().replace(" ", "_")}').config(text=local_time)
            except pytz.exceptions.UnknownTimeZoneError:
                print(f"Error: Invalid timezone {tz_name}")

        if self.stopwatch_running:
            self.stopwatch_time += 1
            hours = self.stopwatch_time // 3600
            minutes = (self.stopwatch_time % 3600) // 60
            seconds = self.stopwatch_time % 60
            self.stopwatch_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")

        if self.timer_running and self.timer_remaining > 0:
            self.timer_remaining -= 1
            hours = self.timer_remaining // 3600
            minutes = (self.timer_remaining % 3600) // 60
            seconds = self.timer_remaining % 60
            self.timer_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
            if self.timer_remaining == 0:
                self.timer_running = False
                self.window.bell()

        self.window.after(1000, self.update_clock)

if __name__ == "__main__":
    app = ClockApp()
    app.window.mainloop()