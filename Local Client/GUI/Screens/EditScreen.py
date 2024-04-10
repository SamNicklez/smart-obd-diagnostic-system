from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivymd.app import MDApp
from PrintInColor import printc
from kivymd.uix.button import MDRaisedButton
from kivy.core.window import Window


class EditScreen(Screen):
    def __init__(self, **kwargs):
        super(EditScreen, self).__init__(**kwargs)

        self.available_commands = []
        self.selections = {}
        layout = BoxLayout(orientation='vertical', size_hint=(1, 1))

        self.confirmation_callback = None

        back_button = MDRaisedButton(text="Back to Main Screen", size_hint=(1, None), height=50)
        layout.add_widget(back_button)
        back_button.bind(on_press=self.go_back)

        # GridLayout adjustment for dynamic sizing
        grid_layout = GridLayout(rows=3, cols=2, spacing=(10, 50), size_hint=(1, 1))
        grid_layout.bind(minimum_height=grid_layout.setter('height'), minimum_width=grid_layout.setter('width'))

        # Dynamically create spinners for each component
        self.spinners = {}
        for i in range(1, 7):  # Assuming 3 labels and 3 gauges
            component_label = Label(text=f'Component {i}', size_hint=(1, None), height=30)
            #component_label = Label(text=f'Component {i}', size_hint_y=None, height=30)
            # Adding navigation buttons
            prev_button = Button(text="<", size_hint=(None, 1), width=30)
            next_button = Button(text=">", size_hint=(None, 1), width=30)

            component_spinner = Spinner(
                text='Select Data Point',
                values=self.available_commands,
                size_hint=(1, 1),  # Allow us to set specific size
                size=(420, 44),  # Specify the size of the spinner
                height=44,
                width=420,
                background_color=MDApp.get_running_app().theme_cls.primary_color,
            )
            component_spinner.bind(text=self.on_spinner_select)

            self.spinners[f'data_point_{i}'] = component_spinner

            prev_button.bind(on_press=lambda instance, s=component_spinner: self.navigate_spinner(s, -1))
            next_button.bind(on_press=lambda instance, s=component_spinner: self.navigate_spinner(s, 1))

            # Add each spinner and its label to the grid layout
            #spinner_box = BoxLayout(orientation='vertical', size_hint=(1, None), height=74)  # This box has a fixed height

            #spinner_box.add_widget(component_spinner)

            spinner_box = BoxLayout(orientation='horizontal', size_hint=(1, None), height=74)
            spinner_box.add_widget(prev_button)
            spinner_box.add_widget(component_spinner)
            spinner_box.add_widget(component_label)
            spinner_box.add_widget(next_button)

            grid_layout.add_widget(spinner_box)

        layout.add_widget(grid_layout)

        # MDRaisedButton(
        #             text="Upload Data to Server",
        #             pos_hint={'center_x': 0.5},
        #             size_hint=(1, .3),
        #         )

        confirm_button = MDRaisedButton(text="Confirm Selections", size_hint=(1, None), height=50)
        confirm_button.bind(on_press=self.confirm_selections)
        layout.add_widget(confirm_button)

        self.add_widget(layout)

        self.previous_label_selections = []
        self.previous_gauge_selections = []
        self.previous_selections = {}


        # Create the labels and the spinners

    def go_back(self, instance):
        printc("GUI: Back to main screen")  
        self.manager.current = 'main' 

    def on_spinner_select(self, spinner, text):
        # Here you would handle the logic for when a selection is made, e.g., updating a model or setting
        printc(f'LIVE DATA: Selected {text} for {spinner}')

    def update_available_commands(self, data):
        self.available_commands = data
        for spinner in self.spinners.values():
            spinner.values = data

    # Call a method to update the display with the new selected data
            
    def confirm_selections(self, instance):

        # Assigning the new selections and setting them to the previous if not set by the user
        for name, spinner in self.spinners.items():
            if spinner.text != 'Select Data Point':
                self.selections[name] = spinner.text
            else:
                self.selections[name] = self.previous_selections[name]

        printc("LIVE DATA: Confirmed Selections:", self.selections)

        # Pass the selections back to the main screen
        if self.confirmation_callback:
            self.confirmation_callback(self.selections)

    # Setter for the previous_selections variable
    def set_current_selections(self, current_selections):
        self.previous_selections = current_selections
        printc("LIVE DATA: Settings current selections", self.previous_selections)

    # Navigation method for spinner
    def navigate_spinner(self, spinner, direction):
        if spinner.values:
            current_index = spinner.values.index(spinner.text)
            next_index = (current_index + direction) % len(spinner.values)
            spinner.text = spinner.values[next_index]

