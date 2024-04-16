from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.label import Label

# Define the FlashingButton class
class FlashingButton(MDRaisedButton):
    def __init__(self, **kwargs):
        super(FlashingButton, self).__init__(**kwargs)
        self.flash_state = False
        self.condition = True  # This will start the button flashing immediately
        self.flash_event = Clock.schedule_interval(self.update_flash, 1)  # Flash every second
        self.dialog = None  # Initialize dialog attribute
        self.engine_code = None
        self.engine_explanation = None

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
        # If you have the engine code and explanation ready, you can directly set them
        self.engine_code = "P0301"  # Example engine code
        self.engine_explanation = "Cylinder 1 Misfire Detected"  # Example explanation
        self.show_alert_dialog()

    def show_alert_dialog(self):
        dialog_title = f"Engine Code: {self.engine_code} - {self.engine_explanation}"

        if not self.dialog:
            self.dialog = MDDialog(
                title=dialog_title,
                type="custom",
                content_cls=BoxLayout(orientation='vertical'),
                size_hint=(0.8, None),
                height="200dp",  # Adjust the height as needed to fit your content
                buttons=[
                    MDRaisedButton(
                        text="Close",
                        on_release=self.close_dialog
                    ),
                ],
            )
        else:
            # If the dialog already exists, just update the title
            self.dialog.title = dialog_title
        self.dialog.open()

    def close_dialog(self, *args):
        if self.dialog:
            self.dialog.dismiss()

