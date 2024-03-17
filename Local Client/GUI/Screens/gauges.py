from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from GUI.gauge import Gauge  # Ensure this is correctly imported

class Gauges(Screen):
    def __init__(self, **kwargs):
        super(Gauges, self).__init__(**kwargs)

        # Main layout
        main_layout = FloatLayout()

        self.gauges = []

        self.data = []

        # Back Button to return to the main screen
        back_button = Button(text="Settings", size_hint=(0.2, 0.1), pos_hint={'x': 0, 'top': 1})
        back_button.bind(on_press=self.settings)
        main_layout.add_widget(back_button)

        # Create the "Edit" button
        edit_button = Button(text="Edit", size_hint=(.1, .1), pos_hint={'x': .9, 'top': 1})
        edit_button.bind(on_press=self.on_edit_press)  # Bind the on_edit_press method to handle button press
        main_layout.add_widget(edit_button)  # Add the button to your layout

        # Define gauge labels and positions
        gauge_info = [
            # {"label": "RPM", "pos_hint": {'x': 0.05, 'y': 0.42}},
            # {"label": "Speed", "pos_hint": {'x': 0.375, 'y': 0.42}},
            # {"label": "Engine Load", "pos_hint": {'x': 0.7, 'y': 0.42}},
            {"label": "Fuel Level", "pos_hint": {'x': 0.05, 'y': 0.02}},
            {"label": "Temperature", "pos_hint": {'x': 0.375, 'y': 0.02}},
            {"label": "Pressure", "pos_hint": {'x': 0.7, 'y': 0.02}}
        ]

        for info in gauge_info:
            # Creating and adding gauges to the layout
            gauge = Gauge(value=50, size_gauge=250, size_text=40)
            self.gauges.append(gauge)
            gauge.size_hint = (None, None)  # Specify no size hint to use absolute size
            gauge.pos_hint = info['pos_hint']  # Position gauges using pos_hint
            main_layout.add_widget(gauge)

            # Creating and adding labels directly below gauges
            # Adjusting label position to be slightly above the gauge
            label_pos_y = info['pos_hint']['y'] + 0.15  # Adjust this value as needed to move the label
            label = Label(text=info['label'], size_hint=(None, None), size=('100dp', '20dp'), font_size='24')
            label.pos_hint = {'center_x': info['pos_hint']['x'] + 0.12, 'y': label_pos_y}
            main_layout.add_widget(label)

        self.data_labels = []  # List to hold references to the data labels

        self.data_title_labels = []

        self.data_titles = ["Data Point #1", "Data Point #2", "Data Point #3"]

        self.data_label_points = []

        # Make some labels for text print outs of the data
        data_title_positions = [
            {'center_x': 0.17, 'top': 0.72},
            {'center_x': 0.495, 'top': 0.72},
            {'center_x': 0.82, 'top': 0.72}
        ]

        for title, pos_hint in zip(self.data_titles, data_title_positions):
            # Create a label for displaying data above each gauge
            data_label = Label(text=title, size_hint=(None, None), size=('100dp', '20dp'), font_size='24')
            data_label.pos_hint = pos_hint
            self.data_title_labels.append(data_label)  # Add the label to the list for later reference
            self.add_widget(data_label)  # Add the label to the main layout

        data_label_positions = [
            {'center_x': 0.17, 'top': 0.65},
            {'center_x': 0.495, 'top': 0.65},
            {'center_x': 0.82, 'top': 0.65}
        ]

        for pos_hint in data_label_positions:
            data_label = Label(text="Actual Data", size_hint=(None, None), size=('100dp', '20dp'), font_size='24')
            data_label.pos_hint = pos_hint
            self.data_labels.append(data_label)  # Add the label to the list for later reference
            self.add_widget(data_label)  # Add the label to the main layout

        # Add a title label
        title_label = Label(text="2017 Chevrolet Silverado", size_hint=(None, None), size=('100dp', '20dp'), font_size='32')
        title_label.pos_hint = {'x': 0.5, 'top': .95}
        self.add_widget(title_label)

        self.add_widget(main_layout)

        # Schedule the update method to be called every second
        Clock.schedule_interval(self.update_gauge, 1)

    def settings(self, instance):
        self.manager.current = 'settings'

    def update_gauge(self, dt):
        for gauge in self.gauges:
            if gauge:
                gauge.value += 1
                if gauge.value > 100:
                    gauge.value = 0

        print("Updating gauges with example data")

    def update_data_labels(self, data):
        """
        Updates the text of each data label with new data.
        :param data: A list of strings or numbers, each corresponding to the new text for a data label.
        """
        for label, new_text in zip(self.data_labels, data):
            label.text = f"Data: {new_text}"    

    def on_edit_press(self, instance):
        print("Edit button pressed")  
        self.manager.current = 'edit'  

    def update_data(self, data):
        self.data = data   