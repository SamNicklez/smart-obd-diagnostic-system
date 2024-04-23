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
        self.condition = False  # This will start the button flashing immediately
        self.flash_event = Clock.schedule_interval(self.update_flash, .75)  # Flash every second
        self.dialog = None  # Initialize dialog attribute
        self.engine_codes = []
        self.engine_explanations = []
        self.dtc_state = False # Variable for if there is a code present or not, initially start at not

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
        self.show_alert_dialog()

    def show_alert_dialog(self):
        if self.dtc_state:
            dialog_title = "Engine Codes:\n" + "\n".join(
                f"{code} - {explanation}" for code, explanation in zip(self.engine_codes, self.engine_explanations)
            )
        else:
            dialog_title = "No Engine Codes Present"   

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

    def set_engine_codes(self, codes, explanations):
        """Sets the engine code and its explanation."""
        self.engine_codes = codes
        self.engine_explanations = explanations

        self.set_dtc_state(bool(codes))

        # Update the dialog title if the dialog exists
        if self.dialog:
            self.dialog.title = self._generate_dialog_title()

    def set_flashing(self, flashing):
        """Enables or disables flashing."""
        self.condition = flashing
        # If flashing should stop, reset the button color
        if not flashing:
            self.md_bg_color = self.theme_cls.primary_color

    def set_dtc_state(self, code_present):
        self.dtc_state = code_present
        self.set_flashing(code_present)

    def _generate_dialog_title(self):
        """Generates the dialog title based on the engine code and explanation."""
        return "Engine Codes:\n" + "\n".join(
            f"{code} - {explanation}" for code, explanation in zip(self.engine_codes, self.engine_explanations)
        )
