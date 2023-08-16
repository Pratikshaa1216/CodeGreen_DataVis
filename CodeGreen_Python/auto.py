import subprocess
import time
import webbrowser
from codecarbon import EmissionsTracker
import matplotlib.pyplot as plt
import psutil

def start_dash_application():
    # Replace `app.py` with the filename of your Dash application
    subprocess.Popen(["python", "app_.py"])

    # Open the Dash application in the default web browser
    webbrowser.open("http://127.0.0.1:8050/")


def track_emissions(duration):
    tracker = EmissionsTracker()
    tracker.start()

    # Track emissions for the specified duration (in seconds)
    time.sleep(duration)

    tracker.stop()
    tracker.save_to_csv("emissions.csv")


def shutdown_dash_application():
    # Find the Dash application process by name and terminate it
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'python' and 'app.py' in proc.cmdline():
            print("Dash application process:", proc.info['name'], proc.info['pid'])
            proc.terminate()

    # Find the Chrome browser process by name and terminate it
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'chrome.exe':
            print("Chrome browser process:", proc.info['name'], proc.info['pid'])
            proc.terminate()



def main():
    duration = 90  # Duration in seconds before shutting down the website

    start_dash_application()
    track_emissions(duration)

    shutdown_dash_application()





if __name__ == '__main__':
    main()
