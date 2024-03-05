from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button

class EditScreen(Screen):
    def __init__(self,  **kwargs):
        super(EditScreen, self).__init__(**kwargs)
        
        self.data_points = []  # List of data point options
        self.update_callback = self.update_callback  # Callback function to update gauges

        layout = BoxLayout(orientation='vertical')

        back_button = Button(text="Back to Main Screen", size_hint=(0.2, 0.1), pos_hint={'x': 0, 'top': 1})
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.spinners = []  # Keep track of all spinners
        for i in range(6):
            spinner = Spinner(
                text='Select Data Point',
                values=self.data_points,
                size_hint=(.5, 0.15),
            )
            self.spinners.append(spinner)
            layout.add_widget(spinner)

        confirm_button = Button(text="Confirm Selections", size_hint=(.5, 0.15))
        confirm_button.bind(on_press=self.on_confirm)
        layout.add_widget(confirm_button)

        self.add_widget(layout)

    def on_confirm(self, instance):
        selections = [spinner.text for spinner in self.spinners]
        self.update_callback(selections)  # Call the callback function with the selections
        self.manager.current = 'gauges'  # Switch back to the gauges screen

    def go_back(self, instance):
        print("Edit button pressed")  
        self.manager.current = 'gauges' 

    def update_callback(selections, test):
        print("Confirm")   