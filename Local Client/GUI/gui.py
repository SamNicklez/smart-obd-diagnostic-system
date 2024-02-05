from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Ellipse
from kivy.clock import Clock
from kivy.properties import NumericProperty
from math import cos, sin, pi

class SpeedGauge(Widget):
    # Speed value, can range from 0 to whatever max speed you want to display, e.g., 200km/h
    speed = NumericProperty(0)

    def __init__(self, **kwargs):
        super(SpeedGauge, self).__init__(**kwargs)
        # Schedule the update of the gauge's display
        Clock.schedule_interval(self.update_gauge, 1)

    def update_gauge(self, dt):
        # Dummy function to simulate speed changes.
        # Replace this with actual speed retrieval from OBD.
        self.speed = (self.speed + 10) % 200  # Example: Cycle speed from 0 to 200
        self.draw_gauge()

    def draw_gauge(self):
        self.canvas.clear()
        with self.canvas:
            # Gauge background
            Color(0.1, 0.1, 0.1)
            Ellipse(pos=self.pos, size=self.size)
            # Gauge fill
            Color(0, 1, 0)  # Green color
            max_angle = 2 * pi * self.speed / 200  # Assuming max speed is 200, adjust accordingly
            for i in range(int(max_angle * 100)):  # Increase 100 for smoother curves
                angle = i / 100.0
                x = self.center_x + cos(angle) * self.width / 2
                y = self.center_y + sin(angle) * self.height / 2
                Line(points=[self.center_x, self.center_y, x, y], width=1)

class OBDApp(App):
    def build(self):
        return SpeedGauge(size_hint=(None, None), size=(200, 200), pos=(100, 100))

if __name__ == '__main__':
    OBDApp().run()
