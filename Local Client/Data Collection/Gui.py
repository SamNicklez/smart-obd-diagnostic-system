from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner  # Added import for Spinner
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager
from Screens.MainScreen import MainScreen
from Screens.SettingsScreen import SettingsScreen 
from LiveDataLayout import LiveDataLayout


class GuiApplication(App):

    data_collector = None  # This should be set or initialized before `build`

    def build(self):
        # Assuming data_collector is already set up with available_commands
        available_commands = self.data_collector.available_commands if self.data_collector else []

        sm = ScreenManager()
        # Directly pass available_commands fetched from data_collector
        main_screen = MainScreen(name='main', available_commands=available_commands)
        settings_screen = SettingsScreen(name='settings')
        
        sm.add_widget(main_screen)
        sm.add_widget(settings_screen)
        
        # Store ScreenManager for easy access later
        self.sm = sm
        
        return sm

    def on_start(self):
        # Use ScreenManager to access the main_screen and its layout
        main_screen = self.sm.get_screen('main')
        if hasattr(self, 'data_collector') and self.data_collector:
            self.data_collector.update_gui_callback = main_screen.layout.update_data


    def set_data_collector(self, data_collector):
        # Set the update_data method of LiveDataLayout as the callback in DataCollector
        data_collector.update_gui_callback = self.live_data_layout.update_data

    def on_stop(self):
        if hasattr(self, 'data_collector') and self.data_collector:
            self.data_collector.stop_collection()

    def set_data_collector(self, data_collector):
        # Assuming you have a method in data_collector to set the callback
        data_collector.update_gui_callback = self.live_data_layout.update_data

        # Store the data_collector reference if needed for other uses
        self.data_collector = data_collector