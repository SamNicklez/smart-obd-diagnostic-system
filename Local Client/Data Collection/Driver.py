from CollectDataTemp import DataCollector
from Gui import GuiApplication
import threading

def run_data_collection(data_collector):
    data_collector.start_collection()

if __name__ == "__main__":
    data_collector = DataCollector()
    
    # Assuming the data collection is intended to run in its own thread
    data_thread = threading.Thread(target=run_data_collection, args=(data_collector,), daemon=True)
    data_thread.start()

    # Create the GUI application instance
    app = GuiApplication(data_collector=data_collector)
    

    # Now start the app
    app.run()
