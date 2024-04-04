import threading
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.screenmanager import  Screen
from Data_Uploading.wifiConnection import check_internet_connection
from GUI.Screens.WifiPopUp import AddWiFiPopup
#from Data_Uploading.uploadData import 
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivy.metrics import dp


# Screen for settings
class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Label to display internet connection status
        self.connection_status_label = MDLabel(
            text="Checking internet connection...",
            halign="center",  # Align the text to the center
            text_color= "white", # Set text color to white
            font_style="Subtitle1",  # Choose a font style from available options
            size_hint_y=None,  # Disable vertical size hint to set a specific height
            height=dp(35),  # Set the height of the label
            valign="middle"  # Ensure the vertical alignment is set to middle
        )
        layout.add_widget(self.connection_status_label)
        
        # Add padding to ensure the text is vertically centered in its bounding box
        self.connection_status_label.padding_y = dp(10)

        # Ensure the label text is repositioned properly when its size changes
        self.connection_status_label.bind(size=self.connection_status_label.setter('text_size'))
        
        # Update the internet connection status at the start and then periodically
        self.update_connection_status()
        Clock.schedule_interval(self.update_connection_status, 30)  # Check every 30 seconds

        # Upload Data to Server Button
        upload_data_button = MDRaisedButton(
            text="Upload Data to Server",
            pos_hint={'center_x': 0.5},
            size_hint=(1, .3),
        )
        upload_data_button.bind(on_press=self.upload_data)
        layout.add_widget(upload_data_button)

        # Back Button to return to the main screen
        back_button = MDRaisedButton(
            text="Back to Main Screen",
            pos_hint={'center_x': 0.5},
            size_hint=(1, .3),  # Width will fill the screen, height is None
            #height=dp(48),  # Define a fixed height for the button
        )
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        # Add New WiFi Network Button
        add_wifi_button = MDRaisedButton(
            text="Add New WiFi Network",
            size_hint=(None, None),
            pos_hint={'center_x': 0.5},
        )
        add_wifi_button.bind(on_press=self.show_add_wifi_popup)
        layout.add_widget(add_wifi_button)
        
        self.add_widget(layout)

    def show_add_wifi_popup(self, instance):
        print("show_add_wifi_popup called")  # Debug print
        popup = AddWiFiPopup()
        popup.open()

    # Method for going back to the main screen
    def go_back(self, instance):
        self.manager.current = 'main'

    # Method for uploading the data to the online server
    def upload_data(self, instance):
        print("Upload the Data")
        if check_internet_connection():
            print("Connected to the internet, ready to upload data")
            # TODO Call the method to upload data to online database
            pass

    def check_connection_status_threaded(self):
        if check_internet_connection():
             self.connection_status_label.text = "Internet Connection: Connected"
        else:
            self.connection_status_label.text = "Internet Connection: Disconnected"
    
    # Method for updating the internet connection status using the wifiConnection files' check_internet_connection method
    def update_connection_status(self, *args):
        threading.Thread(target=self.check_connection_status_threaded).start() 