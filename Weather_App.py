#-------------------------------------------------------------------------------
# Name:        Weather App
# Purpose:     Can check weather of your city
#
# Author:      ADITYA
#
# Created:     19/02/2025
# Copyright:   (c) ADITYA 2025
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView

# API Key and Base URL
API_KEY = "25f6baa2d12cd0cef13fe45fad1839f8"  # Replace with your actual API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Theme Colors
LIGHT_THEME = {
    "bg": [1, 1, 1, 1],  # White
    "fg": [0, 0, 0, 1],  # Black
    "button_bg": [0.9, 0.9, 0.9, 1],  # Light Gray
    "button_fg": [0, 0, 0, 1],  # Black
    "entry_bg": [0.95, 0.95, 0.95, 1],  # Very Light Gray
    "entry_fg": [0, 0, 0, 1],  # Black
}

DARK_THEME = {
    "bg": [0.1, 0.1, 0.1, 1],  # Dark Gray
    "fg": [1, 1, 1, 1],  # White
    "button_bg": [0.2, 0.2, 0.2, 1],  # Dark Gray
    "button_fg": [1, 1, 1, 1],  # White
    "entry_bg": [0.3, 0.3, 0.3, 1],  # Gray
    "entry_fg": [1, 1, 1, 1],  # White
}

# Global variable to track the current theme
current_theme = LIGHT_THEME


class WeatherApp(App):
    def build(self):
        self.title = "Weather App"
        self.root_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # City Input
        self.city_entry = TextInput(
            hint_text="Enter city name",
            multiline=False,
            size_hint_y=None,
            height=40,
            font_size=16,
        )
        self.root_layout.add_widget(self.city_entry)

        # Fetch Button
        self.search_button = Button(
            text="Get Weather",
            size_hint_y=None,
            height=40,
            font_size=16,
        )
        self.search_button.bind(on_press=self.fetch_weather)
        self.root_layout.add_widget(self.search_button)

        # Theme Toggle Button
        self.theme_button = ToggleButton(
            text="Toggle Dark Mode",
            size_hint_y=None,
            height=40,
            font_size=16,
        )
        self.theme_button.bind(on_press=self.toggle_theme)
        self.root_layout.add_widget(self.theme_button)

        # Weather Result Display
        self.result_label = Label(
            text="Weather information will appear here.",
            size_hint_y=None,
            font_size=14,
            halign="left",
            valign="top",
        )
        self.result_label.bind(size=self.result_label.setter('text_size'))
        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height * 0.5))
        scroll_view.add_widget(self.result_label)
        self.root_layout.add_widget(scroll_view)

        # Apply initial theme after widgets are created
        self.apply_theme()

        return self.root_layout

    def fetch_weather(self, instance):
        """Fetches weather and updates the GUI."""
        city = self.city_entry.text
        if not city:
            self.result_label.text = "Please enter a city name."
            return

        weather = self.get_weather(city)

        if "Error" in weather:
            self.result_label.text = weather
        else:
            self.result_label.text = weather

    def get_weather(self, city):
        """Fetches weather details for a given city."""
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"  # Use 'imperial' for Fahrenheit
        }

        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if response.status_code == 200:
            weather_info = (
                f"City: {data['name']}\n"
                f"Temperature: {data['main']['temp']}°C\n"
                f"Weather: {data['weather'][0]['description'].capitalize()}\n"
                f"Humidity: {data['main']['humidity']}%\n"
                f"Wind Speed: {data['wind']['speed']} m/s"
            )
            return weather_info
        else:
            return f"Error: {data.get('message', 'Invalid city name')}"

    def toggle_theme(self, instance):
        """Switches between light and dark themes."""
        global current_theme
        if current_theme == LIGHT_THEME:
            current_theme = DARK_THEME
        else:
            current_theme = LIGHT_THEME

        self.apply_theme()

    def apply_theme(self):
        """Applies the current theme to all widgets."""
        self.root_layout.canvas.before.clear()
        with self.root_layout.canvas.before:
            Window.clearcolor = current_theme["bg"]

        self.city_entry.background_color = current_theme["entry_bg"]
        self.city_entry.foreground_color = current_theme["entry_fg"]
        self.search_button.background_color = current_theme["button_bg"]
        self.search_button.color = current_theme["button_fg"]
        self.theme_button.background_color = current_theme["button_bg"]
        self.theme_button.color = current_theme["button_fg"]
        self.result_label.color = current_theme["fg"]


# Run the Kivy App
if __name__ == "__main__":
    WeatherApp().run()