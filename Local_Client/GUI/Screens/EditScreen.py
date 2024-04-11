from PrintInColor import printc
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner


class EditScreen(Screen):
    def __init__(self, **kwargs):
        super(EditScreen, self).__init__(**kwargs)

        self.available_commands = []
        self.selections = {}
        layout = BoxLayout(orientation='vertical')

        self.confirmation_callback = None

        back_button = Button(text="Back to Main Screen", size_hint=(0.2, 0.1), pos_hint={'x': 0, 'top': 1})
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        # Dynamically create spinners for each component
        self.spinners = {}
        for i in range(1, 7):  # Assuming 3 labels and 3 gauges
            if i <= 3:
                component_label = Label(text=f'Label {i}', size_hint_y=None, height=30)
            else:
                component_label = Label(text=f'Gauge {i - 3}', size_hint_y=None, height=30)
            component_spinner = Spinner(
                text='Select Data Point',
                values=self.available_commands,
                size_hint=(1, None),
                height=44
            )
            component_spinner.bind(text=self.on_spinner_select)

            self.spinners[f'data_point_{i}'] = component_spinner

            layout.add_widget(component_label)
            layout.add_widget(component_spinner)

        confirm_button = Button(text="Confirm Selections", size_hint=(1, 0.1), pos_hint={'center_x': 0.5})
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
