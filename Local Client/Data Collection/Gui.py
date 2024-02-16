# GuiApp.py

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class GuiApplication(App):
    def __init__(self, data_collector, **kwargs):
        super().__init__(**kwargs)
        self.data_collector = data_collector
        
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        # Example widget
        self.label = Label(text='Waiting for data...')
        self.layout.add_widget(self.label)
        return self.layout

    def on_stop(self):
        # Assuming you have a data_collector instance accessible here
        self.data_collector.stop_collection()

    def update_data(self, data):
        # Method to update the GUI with new data
        self.label.text = f"New data: {data}"
