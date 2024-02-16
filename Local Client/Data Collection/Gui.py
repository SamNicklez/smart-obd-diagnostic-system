from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock

class LiveDataLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        # Create labels for different data points
        self.speed_label = Label(text='Speed: Waiting for data...')
        self.rpm_label = Label(text='RPM: Waiting for data...')
        self.coolant_temp_label = Label(text='Coolant Temp: Waiting for data...')

        # Add the labels to the layout
        self.add_widget(self.speed_label)
        self.add_widget(self.rpm_label)
        self.add_widget(self.coolant_temp_label)

    def update_data(self, data):
        # This method will be called from the DataCollector via a callback
        # Use Clock.schedule_once to ensure updates happen on the main thread
        Clock.schedule_once(lambda dt: self._update_labels(data))

    def _update_labels(self, data):
        # Update each label with the new data
        if 'SPEED' in data:
            self.speed_label.text = f"Speed: {data['SPEED']} MPH"
        if 'RPM' in data:
            self.rpm_label.text = f"RPM: {data['RPM']}"
        if 'COOLANT_TEMP' in data:
            self.coolant_temp_label.text = f"Coolant Temp: {data['COOLANT_TEMP']} °C"

    def update_display(self, data):
        # Code to update widgets with new data
        pass

class GuiApplication(App):
    def build(self):
        self.title = 'Vehicle Data Display'
        self.live_data_layout = LiveDataLayout()
        return self.live_data_layout

    def on_start(self):
        # Correctly set the callback to LiveDataLayout's update_data method
        if hasattr(self, 'data_collector'):
            self.data_collector.update_gui_callback = self.live_data_layout.update_data

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