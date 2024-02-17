from LiveDataLayout import LiveDataLayout
from kivy.uix.screenmanager import Screen

# Screen containing the live data and settings button
class MainScreen(Screen):
    def __init__(self, available_commands=[], **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.layout = LiveDataLayout(available_commands=available_commands)
        self.add_widget(self.layout)  