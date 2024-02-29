import threading
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.screenmanager import  Screen
from Data_Uploading.wifiConnection import check_internet_connection
from GUI.Screens.WifiPopUp import AddWiFiPopup
#from Data_Uploading.uploadData import 

# Screen for settings
class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        
        # Label to display internet connection status
        self.connection_status_label = Label(text="Checking internet connection...")
        layout.add_widget(self.connection_status_label)
        
        # Update the internet connection status at the start and then periodically
        self.update_connection_status()
        Clock.schedule_interval(self.update_connection_status, 30)  # Check every 30 seconds

        # Upload Data to Server Button
        upload_data_button = Button(text="Upload Data to Server")
        upload_data_button.bind(on_press=self.upload_data)
        layout.add_widget(upload_data_button)

        # Back Button to return to the main screen
        back_button = Button(text="Back to Main Screen")
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        # Add New WiFi Network Button
        add_wifi_button = Button(text="Add New WiFi Network", size_hint=(None, None), size=(200, 50))
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