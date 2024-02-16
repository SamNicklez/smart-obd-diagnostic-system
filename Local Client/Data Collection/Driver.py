# Driver.py
from CollectDataTemp import DataCollector
from Gui import GuiApplication
import threading

def run_data_collection(data_collector):
    try:
        data_collector.start_collection()
    except KeyboardInterrupt:
        print("Data collection interrupted by user.")
        data_collector.stop_collection()

if __name__ == "__main__":
    data_collector = DataCollector()
    app = GuiApplication()
    app.data_collector = data_collector  # Pass the DataCollector instance to the app
    
    # Assuming the data collection is intended to run in its own thread
    data_thread = threading.Thread(target=run_data_collection, args=(data_collector,), daemon=True)
    data_thread.start()

    # Start the app; on_start method inside GuiApplication will handle setting the callback
    try:
        app.run()
    except KeyboardInterrupt:
        print("GUI application interrupted by user.")
        data_collector.stop_collection()
