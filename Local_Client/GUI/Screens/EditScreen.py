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

        # Dynamically create spinners and labels for each component
        self.spinners = {}
        for i in range(1, 7):  # Assuming 3 labels and 3 gauges
            # Choose the label text based on the index
            label_text = f'Label {i}' if i <= 3 else f'Gauge {i - 3}'
            component_label = Label(text=label_text, size_hint=(1, 1), height=30)

            # Create navigation buttons
            prev_button = Button(text="<", size_hint=(None, 1), width=30)
            next_button = Button(text=">", size_hint=(None, 1), width=30)

            # Create the spinner
            component_spinner = Spinner(
                text='Select Data Point',
                values=self.available_commands,
                size_hint=(1, 1),  # Specify no size hint to use exact size
                size=(420, 44),  # Specify the size of the spinner
                height=44,
                background_color=MDApp.get_running_app().theme_cls.primary_color,
            )
            component_spinner.bind(text=self.on_spinner_select)

            # Save the spinner in a dictionary with a unique key
            self.spinners[f'data_point_{i}'] = component_spinner

            # Bind navigation buttons to spinner navigation method
            prev_button.bind(on_press=lambda instance, s=component_spinner: self.navigate_spinner(s, -1))
            next_button.bind(on_press=lambda instance, s=component_spinner: self.navigate_spinner(s, 1))

            # Create a vertical BoxLayout for the label and spinner
            spinner_box = BoxLayout(orientation='vertical', size_hint=(1, None), size=(420, 74))
            spinner_box.add_widget(component_label)  # Add the label first so it's on top
            spinner_box.add_widget(component_spinner)  # Then the spinner

            # Create a horizontal BoxLayout to include the navigation buttons and the vertical spinner_box
            navigation_and_spinner_box = BoxLayout(orientation='horizontal', size_hint=(1, None), height=74)
            navigation_and_spinner_box.add_widget(prev_button)
            navigation_and_spinner_box.add_widget(spinner_box)
            navigation_and_spinner_box.add_widget(next_button)

            # Add the horizontal BoxLayout to the grid layout
            grid_layout.add_widget(navigation_and_spinner_box)

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
                # TODO check if a gauge value is being set to a string value
                printc("LIVE DATA: ", name)
                if int(name[-1]) > 3:
                     # TODO this means its a gauge
                    pass
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
        # First, ensure there are available values to navigate through
        if not spinner.values:  # Check if the list is empty
            printc("No values loaded in spinner yet.")  # Optional: Inform the user, or log
            return  # Exit the method as there's nothing to navigate

        try:
            current_index = spinner.values.index(spinner.text)
        except ValueError:
            # If current text is not in values, we set a default based on available actions
            if direction > 0 and spinner.values:
                spinner.text = spinner.values[0]  # Go to the first item if moving next
            elif spinner.values:
                spinner.text = spinner.values[-1]  # Go to the last item if moving previous
        else:
            next_index = (current_index + direction) % len(spinner.values)
            spinner.text = spinner.values[next_index]

