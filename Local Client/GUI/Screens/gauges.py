from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty
from kivy.app import App
from GUI.gauge import Gauge
from GUI.Screens import EditScreen
from itertools import islice

class Gauges(Screen):
    available_commands = ListProperty([])
    def __init__(self, edit_screen, **kwargs):
        super(Gauges, self).__init__(**kwargs)

        self.available_commands = kwargs.pop('available_commands', [])
        print("Available commands: " + str(self.available_commands))

        self.edit_screen = edit_screen

        # set a callback function for the edit screen class to use to update the dashboard
        self.edit_screen.confirmation_callback = self.handle_new_selections

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
            {"label": "Gauge 1", "pos_hint": {'x': 0.05, 'y': 0.02}},
            {"label": "Gauge 2", "pos_hint": {'x': 0.375, 'y': 0.02}},
            {"label": "Gauge 3", "pos_hint": {'x': 0.7, 'y': 0.02}}
        ]

        self.gauge_labels = []

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
            self.gauge_labels.append(label)
            main_layout.add_widget(label) 

        self.data_labels = []  # List to hold references to the data labels

        self.data_title_labels = [] # List to hold references to the titles of the data points

        self.current_selections = {'data_point_1': "Coolant Temp", 'data_point_2': "RPM", 'data_point_3': "Speed", 'data_point_4': "Engine Load", 'data_point_5': "Relative Throttle Position", 'data_point_6': "Speed"}

        self.data_label_points = [] # List of the actual data from the selected data points

        self.available_dict = {}

        # Make some labels for text print outs of the data
        data_title_positions = [
            {'center_x': 0.17, 'top': 0.72},
            {'center_x': 0.495, 'top': 0.72},
            {'center_x': 0.82, 'top': 0.72}
        ]

        for title, pos_hint in zip(self.current_selections, data_title_positions):
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

        self.edit_screen.set_current_selections(self.current_selections)

    def settings(self, instance):
        App.get_running_app().root.current = 'settings' 

    def update_gauge(self, data):
        i = 1
        for gauge in self.gauges:
            name = self.current_selections["data_point_" + str(i+3)]
            print("Name: " + str(name))
            data_point = self.find_command_by_name(name) 
            value = data.get(data_point, {'value': 'Not available', 'unit': ''})
            unit = value['unit']
            value = value['value']
            print(str(value))
            if value == 'Not available':
                value = -100
            gauge.value = int(value)

            self.gauge_labels[i - 1].text = f"{str(name)} {unit}"
            i = i + 1

        print("Updating gauges with example data")

    def update_data_labels(self, data):
        self.update_gauge(data) 

        print("HERE DUMBY: " + str(self.current_selections))

        for key in list(self.current_selections.keys())[:3]:
            name = self.current_selections[key]
            data_point = self.find_command_by_name(name)
            value = data.get(data_point, {'value': 'Not available', 'unit': ''})
            index = int(key.split('_')[-1]) - 1
            self.data_labels[index].text = f"{value['value']} {value['unit']}"
            self.data_title_labels[index].text = str(name)

    def on_edit_press(self, instance):
        print("Edit button pressed")  
        App.get_running_app().root.current = 'edit'  

    def update_data(self, data):
        self.data = data
        # This will be called from the DataCollector by a callback
        # Using the schedule_once to update all the necessary information
        Clock.schedule_once(lambda dt: self.update_data_labels(data))  

    # Method for updating the available commands shown in the spinners
    def update_available_commands(self, new_commands):
        print("Updating commands", [cmd for cmd in new_commands])
        
        # Set the class attribute to the entire dictionary
        self.available_dict = new_commands

        # Extracting the list of command names from the dictionary
        self.available_command_names = [cmd_info['name'] for cmd_key, cmd_info in new_commands.items()] 

        self.edit_screen.update_available_commands(self.available_command_names)

    def find_command_by_name(self, name_to_find):
        for cmd_key, cmd_details in self.available_dict.items():
            if cmd_details["name"] == name_to_find:
                return cmd_details["command"]
        return None  # Return None if no matching name is found
    
    def find_name_by_command(self, command_to_find):
        for cmd_key, cmd_info in self.available_dict.items():
            if cmd_info["command"] == command_to_find:
                return cmd_info["name"]
        return None  # Return None if no matching command is found   
    
    def handle_new_selections(self, selections):
        print("IN THE GAUGES CLASS, New selections received:", selections)

        # Should do some checking to see if some boxes aren't filled out. Could just not change that data point if it's not filled in

        # Update the display with the selected data points

        self.current_selections = dict(selections.items())

        print("HERE: " + str(self.current_selections))
