from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

class AddWiFiPopup(Popup):
    def __init__(self, **kwargs):
        super(AddWiFiPopup, self).__init__(**kwargs)
        self.size_hint = (0.8, 0.5)
        self.title = 'Add New WiFi Network'

        content = BoxLayout(orientation='vertical')
        
        self.ssid_input = TextInput(hint_text='SSID', size_hint_y=None, height=30)
        self.password_input = TextInput(hint_text='Password', password=True, size_hint_y=None, height=30)
        
        add_button = Button(text='Add Network', size_hint_y=None, height=50)
        add_button.bind(on_press=self.add_network)
        
        content.add_widget(self.ssid_input)
        content.add_widget(self.password_input)
        content.add_widget(add_button)
        
        self.content = content

    def add_network(self, instance):
        ssid = self.ssid_input.text
        password = self.password_input.text
        print(f"Adding network: SSID={ssid}, Password={password}")

        # TODO logic to add the entered wifi network to the pi's known networks
        self.dismiss()