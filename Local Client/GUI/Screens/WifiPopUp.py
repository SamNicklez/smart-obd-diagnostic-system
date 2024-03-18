from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

class AddWiFiPopup(Popup):
    def __init__(self, **kwargs):
        # Initialize the Popup
        super(AddWiFiPopup, self).__init__(**kwargs)
        self.size_hint = (0.8, 0.5)
        self.title = 'Add New WiFi Network'

        content = BoxLayout(orientation='vertical')
        
        # Text inputs for the wifi network name and the password
        self.ssid_input = TextInput(hint_text='SSID', size_hint_y=None, height=30)
        self.password_input = TextInput(hint_text='Password', password=True, size_hint_y=None, height=30)
        
        # Button for adding the network
        add_button = Button(text='Add Network', size_hint_y=None, height=50)
        add_button.bind(on_press=self.add_network)
        
        # Add all the widgets to the popup
        content.add_widget(self.ssid_input)
        content.add_widget(self.password_input)
        content.add_widget(add_button)
        
        self.content = content

    # Method that gets called whent the add network button gets clicked
    def add_network(self, instance):
        # Grab the text from the inputs boxes
        ssid = self.ssid_input.text
        password = self.password_input.text
        print(f"Adding network: SSID={ssid}, Password={password}")

        # TODO logic to add the entered wifi network to the pi's known networks
        
        self.dismiss() # close out of the popup