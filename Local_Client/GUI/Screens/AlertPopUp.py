from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView


class AlertPopup(ModalView):
    def __init__(self, message, **kwargs):
        super(AlertPopup, self).__init__(**kwargs)
        self.size_hint = (0.8, 0.4)  # Adjusts size to 80% width and 40% height of the parent
        self.auto_dismiss = False

        layout = BoxLayout(orientation='vertical', padding=10)
        message_label = Label(text=message)
        close_btn = Button(text='Close', size_hint=(1, 0.2))
        close_btn.bind(on_release=self.dismiss)

        layout.add_widget(message_label)
        layout.add_widget(close_btn)

        self.add_widget(layout)


def show_popup_main_thread(message):
    def show_popup(dt):
        popup = AlertPopup(message)
        popup.open()

    Clock.schedule_once(show_popup)
