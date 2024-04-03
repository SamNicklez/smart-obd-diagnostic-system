
@staticmethod
def printc(*args):
    text = " ".join(str(arg) for arg in args)
    # Define ANSI color codes within the method
    colors = {
        "DATABASE:": "\u001b[31m",  # Red
        "GUI:": "\u001b[32m",  # Green
        "SENSOR:": "\u001b[34m",  # Blue
        "LIVE DATA:": "\u001b[35m",  # Purple
        "CONNECTION:": "\u001b[33m",  # Yellow
        "reset": "\u001b[0m"  # Resets the color to default
    }

    # Identify the key phrase including the colon
    key_phrase = next((kp for kp in colors if text.startswith(kp)), None)
        
    if key_phrase:
        # If a key phrase is found, print with the corresponding color
        print(f"{colors[key_phrase]}{text}{colors['reset']}")
    else:
        # If no key phrase is matched, print the text with the default color
        print(text)    
