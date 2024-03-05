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

        # Back Button to return to the main screen
        back_button = Button(text="Back to Main Screen", size_hint=(0.2, 0.1), pos_hint={'x': 0, 'top': 1})
        back_button.bind(on_press=self.go_back)
        main_layout.add_widget(back_button)

        # Create the "Edit" button
        edit_button = Button(text="Edit", size_hint=(.1, .1), pos_hint={'x': .9, 'top': 1})
        edit_button.bind(on_press=self.on_edit_press)  # Bind the on_edit_press method to handle button press
        main_layout.add_widget(edit_button)  # Add the button to your layout

        # Define gauge labels and positions
        gauge_info = [
            {"label": "RPM", "pos_hint": {'x': 0.05, 'y': 0.42}},
            {"label": "Speed", "pos_hint": {'x': 0.375, 'y': 0.42}},
            {"label": "Engine Load", "pos_hint": {'x': 0.7, 'y': 0.42}},
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

        self.add_widget(main_layout)

        # Schedule the update method to be called every 0.5 seconds
        Clock.schedule_interval(self.update_gauge, 0.5)

    def go_back(self, instance):
        self.manager.current = 'main'

    def update_gauge(self, dt):
        for gauge in self.gauges:
            if gauge:
                gauge.value += 1
                if gauge.value > 100:
                    gauge.value = 0

        print("Updating gauges with example data")

    def on_edit_press(self, instance):
        print("Edit button pressed")  
        self.manager.current = 'edit'  