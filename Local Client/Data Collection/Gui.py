from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner  # Added import for Spinner
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen

# Screen containing the live data and settings button
class MainScreen(Screen):
    def __init__(self, available_commands=[], **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.layout = LiveDataLayout(available_commands=available_commands)
        self.add_widget(self.layout)

# Screen for settings
class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text="Settings Page - Placeholder"))
        back_button = Button(text="Back to Main Screen")
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'main'

class LiveDataLayout(BoxLayout):
    def __init__(self, **kwargs):
        # Extract available_commands from kwargs and remove it to prevent the TypeError
        available_commands = kwargs.pop('available_commands', [])
        super().__init__(**kwargs)
        
        
        self.orientation = 'vertical'
        # Dictionary to hold the current selections for each spinner
        self.current_selections = {'data_point_1': None, 'data_point_2': None, 'data_point_3': None}

        # Create and add spinners to the layout
        self.spinner1 = self.create_spinner('data_point_1', available_commands)
        self.spinner2 = self.create_spinner('data_point_2', available_commands)
        self.spinner3 = self.create_spinner('data_point_3', available_commands)

        # Create and add labels for displaying data
        self.label1 = Label(text='Data Point 1: Waiting for data...')
        self.label2 = Label(text='Data Point 2: Waiting for data...')
        self.label3 = Label(text='Data Point 3: Waiting for data...')

        # Add widgets to the layout
        self.add_widget(self.spinner1)
        self.add_widget(self.label1)
        self.add_widget(self.spinner2)
        self.add_widget(self.label2)
        self.add_widget(self.spinner3)
        self.add_widget(self.label3)

        # Modify the settings button initialization
        settings_button = Button(text='Settings', size_hint=(None, None), size=(100, 50))
        settings_button.bind(on_press=self.switch_to_settings)
        self.add_widget(settings_button)

    def update_data(self, data):
        # This method will be called from the DataCollector via a callback
        # Use Clock.schedule_once to ensure updates happen on the main thread
         Clock.schedule_once(lambda dt: self._update_labels(data))

    def on_spinner_select(self, spinner_id, text):
        # Correctly update the current selection based on spinner_id
        self.current_selections[spinner_id] = text
        # Decide which label to update based on the spinner_id
        label_to_update = getattr(self, f'label{spinner_id[-1]}')
        label_to_update.text = f"{text}: Waiting for data..."

    def _update_labels(self, data):
        for i, key in enumerate(self.current_selections, start=1):
            data_point = self.current_selections[key]
            value = data.get(data_point, 'Not available')
            getattr(self, f'label{i}').text = f"{data_point}: {value}"

    def update_display(self, data):
        # Code to update widgets with new data
        pass

    def create_spinner(self, spinner_id, available_commands):
        spinner = Spinner(
            text='Select Data Point',
            values=available_commands,
            size_hint=(None, None),
            size=(200, 44),
            pos_hint={'center_x': 0.5}
        )
        # Ensure spinner_id is correctly captured by using it directly in the lambda function
        spinner.bind(text=lambda spinner, text: self.on_spinner_select(spinner_id, text))
        return spinner

    def _update_selected_data_point(self, data):
        if self.current_data_point in data:
            # Update the label with the value of the selected data point
            value = data[self.current_data_point]
            # Assuming you want to display it on the speed_label or a dedicated label
            self.speed_label.text = f"{self.current_data_point}: {value}"
        else:
            # Handle the case where the data point is not available in the data dictionary
            self.speed_label.text = f"{self.current_data_point}: Not available"

    def switch_to_settings(self, instance):
        App.get_running_app().root.current = 'settings'        

class GuiApplication(App):

    data_collector = None  # This should be set or initialized before `build`

    def build(self):
        # Assuming data_collector is already set up with available_commands
        available_commands = self.data_collector.available_commands if self.data_collector else []

        sm = ScreenManager()
        # Directly pass available_commands fetched from data_collector
        main_screen = MainScreen(name='main', available_commands=available_commands)
        settings_screen = SettingsScreen(name='settings')
        
        sm.add_widget(main_screen)
        sm.add_widget(settings_screen)
        
        # Store ScreenManager for easy access later
        self.sm = sm
        
        return sm

    def on_start(self):
        # Use ScreenManager to access the main_screen and its layout
        main_screen = self.sm.get_screen('main')
        if hasattr(self, 'data_collector') and self.data_collector:
            self.data_collector.update_gui_callback = main_screen.layout.update_data


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