from LiveDataLayout import LiveDataLayout
from kivy.uix.screenmanager import Screen

# Screen containing the live data and settings button
class MainScreen(Screen):
    def __init__(self, available_commands=[], **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        # Initialize the layout
        self.layout = LiveDataLayout(available_commands=available_commands)
        # Add the layout as a widget
        self.add_widget(self.layout)

    # Method that the DataCollector calls to insert new commands that are found
    def update_commands(self, new_commands):
        # Call the method to update the available commands that are shown on the screen
        self.layout.update_available_commands(new_commands) 