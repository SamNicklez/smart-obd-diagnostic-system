from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.label import Label

class EditScreen(Screen):
    def __init__(self, **kwargs):
        super(EditScreen, self).__init__(**kwargs)
        
        self.available_commands = []
        self.selection = []
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
                component_label = Label(text=f'Gauge {i-3}', size_hint_y=None, height=30)
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

        # Create the labels and the spinners

    def go_back(self, instance):
        print("Edit button pressed")  
        self.manager.current = 'main' 

    def on_spinner_select(self, spinner, text):
        # Here you would handle the logic for when a selection is made, e.g., updating a model or setting
        print(f'Selected {text} for {spinner}')

    def update_available_commands(self, data):
        self.available_commands = data
        for spinner in self.spinners.values():
            spinner.values = data

        # Call a method to update the display with the new selected data
            
    def confirm_selections(self, instance):

        # Add a check to see if all the components have a data point in them
        

        self.selections = {name: spinner.text for name, spinner in self.spinners.items()}
        print("Confirmed SELECTIONS:", self.selections)

        if self.confirmation_callback:
            self.confirmation_callback(self.selections)

        # Need to store the selections and some how give them back to the gauges class


               