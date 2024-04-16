from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class DashboardApp(App):
    def build(self):
        # Main layout container
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(1, 1))

        # Speed section
        speed_section = BoxLayout(size_hint=(1, None), height=50)  # Customize the height as needed
        speed_label = Label(text='Speed: 0 km/h')
        speed_section.add_widget(speed_label)

        # Temperature section
        temperature_section = BoxLayout(size_hint=(1, None), height=50)  # Customize the height as needed
        temperature_label = Label(text='Temperature: 20°C')
        temperature_section.add_widget(temperature_label)

        # Third section placeholder
        third_section = BoxLayout(size_hint=(1, None), height=50)  # Customize the height as needed
        third_section_label = Label(text='Third Section Placeholder')
        third_section.add_widget(third_section_label)

        # Add the sections to the main layout
        main_layout.add_widget(speed_section)
        main_layout.add_widget(temperature_section)
        main_layout.add_widget(third_section)

        return main_layout

if __name__ == '__main__':
    DashboardApp().run()
