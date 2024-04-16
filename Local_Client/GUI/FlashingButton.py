from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.clock import Clock

# Define the FlashingButton class
class FlashingButton(Button):
    def __init__(self, **kwargs):
        super(FlashingButton, self).__init__(**kwargs)
        self.flash_state = False
        self.condition = True  # You'll need to set this based on your specific condition
        self.flash_event = Clock.schedule_interval(self.update_flash, 1)

    def update_flash(self, dt):
        if self.condition:
            self.flash_state = not self.flash_state
            if self.flash_state:
                self.background_color = (1, 0, 0, 1)  # Red color
            else:
                self.background_color = (1, 1, 1, 1)  # White color
        else:
            self.background_color = (1, 1, 1, 1)

    def on_press(self):
        # Display a Popup on button press
        content = BoxLayout(orientation='vertical')
        close_btn = Button(text='Close')
        content.add_widget(close_btn)
        popup = Popup(title='Menu', content=content, size_hint=(None, None), size=(400, 400))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()