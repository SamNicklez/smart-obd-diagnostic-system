# Driver.py
from CollectData import DataCollector
from Gui import GuiApplication
import threading

# Method for starting the data collection
def run_data_collection(data_collector):
    try:
        data_collector.start_collection() # start the data collection
    except KeyboardInterrupt:
        print("Data collection interrupted by user.")
        data_collector.stop_collection()

if __name__ == "__main__":
    data_collector = DataCollector() # create a DataCollector
    app = GuiApplication() # create a GuiApplication
    app.data_collector = data_collector  # Pass the DataCollector instance to the app
    
    # Run the data collection on its own thread so it doesn't interrupt the GUI
    data_thread = threading.Thread(target=run_data_collection, args=(data_collector,), daemon=True)
    data_thread.start()

    # Start the gui application
    try:
        app.run()
    except KeyboardInterrupt:
        print("GUI application interrupted by user.")
        data_collector.stop_collection()
