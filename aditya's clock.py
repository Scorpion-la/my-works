#-------------------------------------------------------------------------------
# Name:        Clock
# Purpose:      A simple way to see time
#
# Author:      ADITYA
#
# Created:     15/02/2025
# Copyright:   (c) ADITYA 2025
# Licence:     <your licence>
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.spinner import Spinner
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import ListProperty
from datetime import datetime
import pytz

# Theme Colors
LIGHT_THEME = {
    "bg": [1, 1, 1, 1],  # White
    "fg": [0, 0, 0, 1],  # Black
    "button_bg": [0.9, 0.9, 0.9, 1],  # Light Gray
    "button_fg": [0, 0, 0, 1],  # Black
    "tab_bg": [0.8, 0.8, 0.8, 1],  # Light Gray
    "tab_fg": [0, 0, 0, 1],  # Black
}

DARK_THEME = {
    "bg": [0.1, 0.1, 0.1, 1],  # Dark Gray
    "fg": [1, 1, 1, 1],  # White
    "button_bg": [0.2, 0.2, 0.2, 1],  # Dark Gray
    "button_fg": [1, 1, 1, 1],  # White
    "tab_bg": [0.3, 0.3, 0.3, 1],  # Gray
    "tab_fg": [1, 1, 1, 1],  # White
}

# Global variable to track the current theme
current_theme = LIGHT_THEME


class RoundedButton(Button):
    """Custom Button with rounded corners."""
    border_radius = ListProperty([20])  # Radius for rounded corners

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        self.update_canvas()

    def update_canvas(self, *args):
        """Update the canvas to draw rounded corners."""
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.background_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=self.border_radius)


class ClockApp(App):
    def build(self):
        self.title = "Modern Clock App"
        self.root_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # Tabbed Panel
        self.tabs = TabbedPanel(do_default_tab=False)
        self.root_layout.add_widget(self.tabs)

        # Add Tabs
        self.setup_clock_tab()
        self.setup_stopwatch_tab()
        self.setup_timer_tab()
        self.setup_world_time_tab()

        # Theme Toggle Button
        self.theme_button = RoundedButton(
            text="Toggle Dark Mode",
            size_hint=(None, None),
            size=(150, 40),
            pos_hint={"center_x": 0.5},
        )
        self.theme_button.bind(on_press=self.toggle_theme)
        self.root_layout.add_widget(self.theme_button)

        # Apply initial theme
        self.apply_theme()

        # Start clock updates
        Clock.schedule_interval(self.update_clock, 1)

        return self.root_layout

    def setup_clock_tab(self):
        """Setup the Clock tab."""
        clock_tab = TabbedPanelItem(text="Clock")
        clock_container = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.clock_label = Label(
            text="00:00:00",
            font_size=48,
            bold=True,
        )
        clock_container.add_widget(self.clock_label)

        self.date_label = Label(
            text="Monday, January 1, 2023",
            font_size=16,
        )
        clock_container.add_widget(self.date_label)

        clock_tab.add_widget(clock_container)
        self.tabs.add_widget(clock_tab)

    def setup_stopwatch_tab(self):
        """Setup the Stopwatch tab."""
        stopwatch_tab = TabbedPanelItem(text="Stopwatch")
        stopwatch_container = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.stopwatch_label = Label(
            text="00:00:00",
            font_size=48,
            bold=True,
        )
        stopwatch_container.add_widget(self.stopwatch_label)

        btn_container = BoxLayout(orientation="horizontal", spacing=10, size_hint_y=None, height=50)

        self.start_stopwatch_button = RoundedButton(
            text="Start",
            on_press=self.start_stopwatch,
        )
        btn_container.add_widget(self.start_stopwatch_button)

        self.stop_stopwatch_button = RoundedButton(
            text="Stop",
            on_press=self.stop_stopwatch,
        )
        btn_container.add_widget(self.stop_stopwatch_button)

        self.reset_stopwatch_button = RoundedButton(
            text="Reset",
            on_press=self.reset_stopwatch,
        )
        btn_container.add_widget(self.reset_stopwatch_button)

        stopwatch_container.add_widget(btn_container)
        stopwatch_tab.add_widget(stopwatch_container)
        self.tabs.add_widget(stopwatch_tab)

        self.stopwatch_running = False
        self.stopwatch_time = 0

    def setup_timer_tab(self):
        """Setup the Timer tab."""
        timer_tab = TabbedPanelItem(text="Timer")
        timer_container = BoxLayout(orientation="vertical", padding=10, spacing=10)

        input_container = BoxLayout(orientation="horizontal", spacing=10, size_hint_y=None, height=50)

        self.hours_spinner = Spinner(
            text="00",
            values=[f"{i:02d}" for i in range(24)],
            size_hint=(None, None),
            size=(80, 40),
        )
        input_container.add_widget(self.hours_spinner)

        self.minutes_spinner = Spinner(
            text="00",
            values=[f"{i:02d}" for i in range(60)],
            size_hint=(None, None),
            size=(80, 40),
        )
        input_container.add_widget(self.minutes_spinner)

        self.seconds_spinner = Spinner(
            text="00",
            values=[f"{i:02d}" for i in range(60)],
            size_hint=(None, None),
            size=(80, 40),
        )
        input_container.add_widget(self.seconds_spinner)

        timer_container.add_widget(input_container)

        self.timer_label = Label(
            text="00:00:00",
            font_size=48,
            bold=True,
        )
        timer_container.add_widget(self.timer_label)

        btn_container = BoxLayout(orientation="horizontal", spacing=10, size_hint_y=None, height=50)

        self.start_timer_button = RoundedButton(
            text="Start",
            on_press=self.start_timer,
        )
        btn_container.add_widget(self.start_timer_button)

        self.stop_timer_button = RoundedButton(
            text="Stop",
            on_press=self.stop_timer,
        )
        btn_container.add_widget(self.stop_timer_button)

        self.reset_timer_button = RoundedButton(
            text="Reset",
            on_press=self.reset_timer,
        )
        btn_container.add_widget(self.reset_timer_button)

        timer_container.add_widget(btn_container)
        timer_tab.add_widget(timer_container)
        self.tabs.add_widget(timer_tab)

        self.timer_running = False
        self.timer_remaining = 0

    def setup_world_time_tab(self):
        """Setup the World Time tab."""
        world_time_tab = TabbedPanelItem(text="World Time")
        world_container = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.timezone_labels = {}

        timezones = [
            ('US/Pacific', 'San Francisco'),
            ('US/Eastern', 'New York'),
            ('Europe/London', 'London'),
            ('Asia/Tokyo', 'Tokyo'),
            ('Australia/Sydney', 'Sydney')
        ]

        for tz, city_label in timezones:
            frame = BoxLayout(orientation="horizontal", spacing=10, size_hint_y=None, height=40)

            label = Label(
                text=f"{city_label}: 00:00:00",
                font_size=16,
            )
            frame.add_widget(label)
            self.timezone_labels[city_label] = label

            world_container.add_widget(frame)

        world_time_tab.add_widget(world_container)
        self.tabs.add_widget(world_time_tab)

    def start_stopwatch(self, instance):
        self.stopwatch_running = True

    def stop_stopwatch(self, instance):
        self.stopwatch_running = False

    def reset_stopwatch(self, instance):
        self.stopwatch_running = False
        self.stopwatch_time = 0
        self.stopwatch_label.text = "00:00:00"

    def start_timer(self, instance):
        try:
            hours = int(self.hours_spinner.text)
            minutes = int(self.minutes_spinner.text)
            seconds = int(self.seconds_spinner.text)
            total_seconds = hours * 3600 + minutes * 60 + seconds
            if total_seconds <= 0:
                raise ValueError("Time must be positive")
            self.timer_remaining = total_seconds
            self.timer_running = True
        except ValueError:
            print("Invalid input for timer")

    def stop_timer(self, instance):
        self.timer_running = False

    def reset_timer(self, instance):
        self.timer_running = False
        self.hours_spinner.text = "00"
        self.minutes_spinner.text = "00"
        self.seconds_spinner.text = "00"
        self.timer_remaining = 0
        self.timer_label.text = "00:00:00"

    def toggle_theme(self, instance):
        """Toggle between light and dark themes."""
        global current_theme
        if current_theme == LIGHT_THEME:
            current_theme = DARK_THEME
        else:
            current_theme = LIGHT_THEME

        self.apply_theme()

    def apply_theme(self):
        """Apply the current theme to all widgets."""
        Window.clearcolor = current_theme["bg"]

        for widget in self.root_layout.walk():
            if isinstance(widget, Label):
                widget.color = current_theme["fg"]
            elif isinstance(widget, (Button, RoundedButton)):
                widget.background_color = current_theme["button_bg"]
                widget.color = current_theme["button_fg"]
            elif isinstance(widget, TabbedPanel):
                widget.background_color = current_theme["tab_bg"]
                widget.tab_background_color = current_theme["tab_bg"]
                widget.tab_color = current_theme["tab_fg"]

    def update_clock(self, dt):
        """Update the clock, stopwatch, timer, and world time."""
        # Update Clock
        now = datetime.now()
        self.clock_label.text = now.strftime("%H:%M:%S")
        self.date_label.text = now.strftime("%A, %B %d, %Y")

        # Update Stopwatch
        if self.stopwatch_running:
            self.stopwatch_time += 1
            hours = self.stopwatch_time // 3600
            minutes = (self.stopwatch_time % 3600) // 60
            seconds = self.stopwatch_time % 60
            self.stopwatch_label.text = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        # Update Timer
        if self.timer_running and self.timer_remaining > 0:
            self.timer_remaining -= 1
            hours = self.timer_remaining // 3600
            minutes = (self.timer_remaining % 3600) // 60
            seconds = self.timer_remaining % 60
            self.timer_label.text = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            if self.timer_remaining == 0:
                self.timer_running = False
                print("Timer finished!")

        # Update World Time
        for city_label, label_widget in self.timezone_labels.items():
            tz_name = None
            for tz, city in [
                ('US/Pacific', 'San Francisco'),
                ('US/Eastern', 'New York'),
                ('Europe/London', 'London'),
                ('Asia/Tokyo', 'Tokyo'),
                ('Australia/Sydney', 'Sydney')
            ]:
                if city == city_label:
                    tz_name = tz
                    break

            if tz_name:
                tz = pytz.timezone(tz_name)
                local_time = datetime.now(tz).strftime("%H:%M:%S")
                label_widget.text = f"{city_label}: {local_time}"


# Run the Kivy App
if __name__ == "__main__":
    ClockApp().run()
