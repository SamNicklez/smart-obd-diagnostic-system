from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog

# Define the FlashingButton class
class FlashingButton(MDRaisedButton):
    def __init__(self, **kwargs):
        super(FlashingButton, self).__init__(**kwargs)
        self.flash_state = False
        self.condition = True  # This will start the button flashing immediately
        self.flash_event = Clock.schedule_interval(self.update_flash, 1)  # Flash every second
        self.dialog = None  # Initialize dialog attribute

    def update_flash(self, dt):
        if self.condition:
            self.flash_state = not self.flash_state
            if self.flash_state:
                self.md_bg_color = (1, 0, 0, 1)  # Red color
            else:
                self.md_bg_color = (1, 1, 1, 1)  # White color
        else:
            self.md_bg_color = self.theme_cls.primary_color  # Reset to default theme color

    def on_press(self):
        # Display a Popup on button press
        self.show_alert_dialog()

    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Menu",
                type="custom",
                content_cls=BoxLayout(orientation='vertical'),
                buttons=[
                    MDRaisedButton(
                        text="Close",
                        on_release=self.close_dialog
                    ),
                ],
            )
        self.dialog.open()

    def close_dialog(self, *args):
        self.dialog.dismiss()
