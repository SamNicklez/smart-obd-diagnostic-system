from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner  # Added import for Spinner
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.properties import ListProperty
from GUI.Screens.AlertPopUp import AlertPopup

class LiveDataLayout(BoxLayout):

    available_commands = ListProperty([])  # Define it as a Kivy property so it automatically updates when the list is changed

    def __init__(self, **kwargs):
        # Get the available commands from the args in the constructor
        self.available_commands = kwargs.pop('available_commands', [])
        super(LiveDataLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # Initialize the data points selections
        self.current_selections = {'data_point_1': None, 'data_point_2': None, 'data_point_3': None}

        # Create the labels and the spinners
        self.create_spinners_and_labels()  # Call this to initially create spinners and labels

        # Create the button for the settings screen
        self.settings_button = Button(text='Settings', size_hint=(None, None), size=(100, 50))
        self.settings_button.bind(on_press=self.switch_to_settings)
        self.add_widget(self.settings_button)

        self.dtc_count = 0

        self.data = []

    # Method for updating the live data on the screen
    def update_data(self, data):
        self.data = data
        # This will be called from the DataCollector by a callback
        # Using the schedule_once to update all the necessary information
        Clock.schedule_once(lambda dt: self.update_information(data))

    def update_information(self, data):

        # Call to update the labels
        self.update_labels(data)

        # TODO add any constraints here that should alert the driver
        # Could make some customizable constraints so the user can set when they want to be alerted

        # Check if any data points out of bounds and alert
        # engine_load = data.get('ENGINE_LOAD', None)

        # if engine_load['value'] is not None and engine_load['value'] > 60:  # Assuming 75 is the threshold
        #     self.show_alert_popup(f"High Engine Load Detected: {engine_load['value']}%") 

        # Checking for dtc codes and alerting if there is a new one
        get_dtc = data.get('GET_DTC', None) 
        get_dtc = get_dtc['value']

        if get_dtc is not None and len(get_dtc) == 2 and self.dtc_count != len(get_dtc):
            self.show_alert_popup("DTC Detected " + " Codes: " + get_dtc)
            self.dtc_count = len(get_dtc)
            #self.add_icon()
            self.add_icon()

            # TODO could add an icon to the screen to show the user that there is a dtc present
        elif get_dtc is not None and len(get_dtc) != 2 and self.dtc_count != 0:
            self.dtc_count = 0
            # TODO clear the dtc present icon

    # Method that runs when a spinner is clicked on
    def on_spinner_select(self, spinner_id, text):
        # Update the selected Data point
        self.current_selections[spinner_id] = text

        # Decide which label to update based on the spinner_id
        label_to_update = getattr(self, f'label{spinner_id[-1]}')
        label_to_update.text = f"{text}: Waiting for data..."

    # Method for updating the labels 
    def update_labels(self, data):
        # Update the labels on the screen with the selected data
        for i, key in enumerate(self.current_selections, start=1):
            data_point = self.current_selections[key]
            value = data.get(data_point, {'value': 'Not available', 'unit': ''})
            getattr(self, f'label{i}').text = f"{data_point}: {value['value']} {value['unit']}"

    # Method for creating the spinners
    def create_spinner(self, spinner_id, available_commands):
        spinner = Spinner (
            text='Select Data Point',
            values=available_commands,
            size_hint=(None, None),
            size=(200, 44),
            pos_hint={'center_x': 0.5}
        )

        # Bind the spinner to run the on_spinner_select method when clicked
        spinner.bind(text=lambda spinner, text: self.on_spinner_select(spinner_id, text))
        return spinner

    # Method for updating the selected data point
    def update_selected_data_point(self, data):
        if self.current_data_point in data:
            # Update the label with the value of the selected data point
            value = data[self.current_data_point]
            
            self.speed_label.text = f"{self.current_data_point}: {value}"
        else:
            # Handle the case where the data point is not available in the data dictionary
            self.speed_label.text = f"{self.current_data_point}: Not available"

    # Method for switching to the settings screen
    def switch_to_settings(self, instance):
        App.get_running_app().root.current = 'settings'  

    # Method for updating the available commands shown in the spinners
    def update_available_commands(self, new_commands):
        print("Updating commands", [cmd for cmd in new_commands])
        self.available_commands = new_commands
        self.create_spinners_and_labels()

    # Method for creating all the spinners and labels
    def create_spinners_and_labels(self):

        # Remove the current spinners so we can replace them
        for widget in self.children[:]:
            if widget is not self.settings_button and widget is not self.icon_button:  # Assuming you have a reference to the settings button
                self.remove_widget(widget)

        # Recreate the spinner widgets and labels with the updated commands
        self.spinner1 = self.create_spinner('data_point_1', self.available_commands)
        self.spinner2 = self.create_spinner('data_point_2', self.available_commands)
        self.spinner3 = self.create_spinner('data_point_3', self.available_commands)

        self.label1 = Label(text='Data Point 1: Waiting for data...')
        self.label2 = Label(text='Data Point 2: Waiting for data...')
        self.label3 = Label(text='Data Point 3: Waiting for data...')

        # Add the newly created widgets to the layout
        self.add_widget(self.spinner1)
        self.add_widget(self.label1)
        self.add_widget(self.spinner2)
        self.add_widget(self.label2)
        self.add_widget(self.spinner3)
        self.add_widget(self.label3)

    def show_alert_popup(self, message):
        popup = AlertPopup(message)
        popup.open()

    def add_icon(self, icon_source='images/DTC_image.png'):
        print("Adding the icon")
        # Create an icon button with the image as its background
        self.icon_button = Button(background_normal=icon_source,
                                size_hint=(None, None),
                                size=('50', '50'))  # Adjust the position as needed

        # Optionally, bind the button to a callback function
        self.icon_button.bind(on_press=self.on_icon_press)

        # Add the icon button to the layout
        self.add_widget(self.icon_button)    

    def on_icon_press(self, instance):
        # Handle the icon press event
        print("Icon pressed!")

        get_dtc = self.data.get('GET_DTC', None) 
        get_dtc = get_dtc['value']
    
        self.show_alert_popup("Engine Codes Present: " + get_dtc)

    def remove_icon(self):
        # Remove the icon here
        self.remove_widget(self.icon_button)