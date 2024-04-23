from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.gridlayout import GridLayout
from kivymd.uix.label import MDLabel


class FullScreenApp(MDApp):
    def build(self):
        # Main layout with flexible sizing
        layout = GridLayout(cols=3, size_hint=(1, 1), padding="10dp", spacing="10dp")

        # Define the sections
        sections = ['Speed', 'Temperature', 'Section 3', 'Section 4', 'Section 5', 'Section 6']

        # Create and add cards for each section, making them fill their space
        for section in sections:
            card = MDCard(elevation=8, radius=[15], size_hint=(0.5, 0.33), padding="10dp")
            card.add_widget(
                MDLabel(text=section, halign='center', theme_text_color='Primary', size_hint_y=None, height=20))
            layout.add_widget(card)

        return layout


if __name__ == '__main__':
    FullScreenApp().run()
