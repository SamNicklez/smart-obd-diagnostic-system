from gpiozero import Button
from signal import pause

def when_pressed():
    print("Button was pressed!")

button = Button(17)  # Replace 3 with your GPIO pin number if different

button.when_pressed = when_pressed

pause()  # This will keep the script running to detect button presses