#-------------------------------------------------------------------------------
# Name:        Wifi_Password_extractor
# Purpose:     Extract saved wifi passwords
#
# Author:      ADITYA
#
# Created:     22/02/2025
# Copyright:   (c) ADITYA 2025
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import subprocess
import re
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window

class WiFiPasswordExtractor(App):
    def build(self):
        self.title = "WiFi Password Extractor"
        self.root_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # Title Label
        title_label = Label(
            text="WiFi Password Extractor",
            font_size=24,
            size_hint_y=None,
            height=50,
        )
        self.root_layout.add_widget(title_label)

        # Scrollable Results Area
        self.results_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.results_layout.bind(minimum_height=self.results_layout.setter('height'))

        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height * 0.7))
        scroll_view.add_widget(self.results_layout)
        self.root_layout.add_widget(scroll_view)

        # Extract Button
        extract_button = Button(
            text="Extract WiFi Passwords",
            size_hint_y=None,
            height=50,
        )
        extract_button.bind(on_press=self.extract_wifi_passwords)
        self.root_layout.add_widget(extract_button)

        return self.root_layout

    def extract_wifi_passwords(self, instance):
        """Extract and display saved WiFi passwords."""
        self.results_layout.clear_widgets()  # Clear previous results

        try:
            # Run the command to get saved WiFi profiles
            profiles_output = subprocess.run(
                ["netsh", "wlan", "show", "profiles"],
                capture_output=True,
                text=True,
            ).stdout

            # Extract profile names using regex
            profile_names = re.findall(r":\s(.*)", profiles_output)

            if not profile_names:
                self.results_layout.add_widget(Label(text="No WiFi profiles found.", font_size=16))
                return

            # Loop through each profile and extract the password
            for profile in profile_names:
                try:
                    # Get the password for the profile
                    profile_output = subprocess.run(
                        ["netsh", "wlan", "show", "profile", f"name={profile}", "key=clear"],
                        capture_output=True,
                        text=True,
                    ).stdout

                    # Extract the password using regex
                    password_match = re.search(r"Key Content\s*:\s(.*)", profile_output)
                    password = password_match.group(1).strip() if password_match else "Not Available"

                    # Add the result to the layout
                    result_label = Label(
                        text=f"WiFi: {profile}\nPassword: {password}",
                        font_size=16,
                        size_hint_y=None,
                        height=60,
                    )
                    self.results_layout.add_widget(result_label)

                except Exception as e:
                    print(f"Error extracting password for {profile}: {e}")

        except Exception as e:
            self.results_layout.add_widget(Label(text=f"Error: {str(e)}", font_size=16))


# Run the Kivy App
if __name__ == "__main__":
    WiFiPasswordExtractor().run()