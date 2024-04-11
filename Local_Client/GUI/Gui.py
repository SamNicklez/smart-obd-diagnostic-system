from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
Config.set('graphics', 'fullscreen', 1)
from GUI.Screens.MainScreen import MainScreen
from GUI.Screens.SettingsScreen import SettingsScreen
from GUI.Screens.DataDashboard import Dashboard
from GUI.Screens.EditScreen import EditScreen
from kivymd.app import MDApp
from kivy.graphics import Color, Rectangle


# Main GUI class that starts and runs the GUI application
class GuiApplication(MDApp):
    data_collector = None  # This should be set or initialized before `build`

    def build(self):

        # set the available commands to the 
        available_commands = self.data_collector.filtered_commands if self.data_collector else set()

        # Schedule the update_supported_commands to run every second to wait for the DataCollector to grab the available commands for the current car
        Clock.schedule_interval(self.update_supported_commands, 1)

        # Initialize a ScreenManager to control the different screens
        self.sm = ScreenManager()

        edit_screen = EditScreen(name='edit')
        dashboard = Dashboard(name='dashboard', edit_screen=edit_screen)

        # Set the two different screens
        self.main_screen = MainScreen(name='main', available_commands=available_commands, dashboard=dashboard)
        settings_screen = SettingsScreen(name='settings')

        # Add the widgets
        self.sm.add_widget(self.main_screen)
        self.sm.add_widget(settings_screen)
        self.sm.add_widget(edit_screen)

        # Add a callback for the DataCollector to update data on the main screen
        if hasattr(self, 'data_collector'):
            self.data_collector.update_gui_callback = self.main_screen.layout.update_data

        # Set the background color
        with self.sm.canvas.before:
            Color(0.16, 0.16, 0.16, 1)  # Dark gray as an example
            self.rect = Rectangle(size=self.sm.size, pos=self.sm.pos)

        self.sm.bind(size=self._update_background, pos=self._update_background)

        return self.sm

    def _update_background(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    # Method that runs when the Gui is closed
    def on_stop(self):
        if hasattr(self, 'data_collector') and self.data_collector:
            self.data_collector.stop_collection()  # Stop the collection when the gui is closed

    # Method for updating the supported commands
    def update_supported_commands(self, dt):
        if self.data_collector.filtered_commands:  # if it sees the filtered_commands variable in the DataCollector class
            # Retrieve the current list of filtered commands
            filtered_commands = self.data_collector.filter_supported_commands()

            # Ensure filtered_commands is a list, even if empty
            # filtered_commands = filtered_commands if filtered_commands is not None else []

            # Now that filtered_commands is guaranteed to be a list, update the commands in MainScreen
            self.main_screen.update_commands(filtered_commands)

            # Stop calling this method since it has the filtered_commands variable intialized meaning the 
            # data_collector has set the available commands
            Clock.unschedule(self.update_supported_commands)
