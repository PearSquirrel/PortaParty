from blynk_api import WinchController
import time

# testing the API for the winch - Joffen
winch = WinchController()

winch.lower_winch()
print("Lowering winch...")
time.sleep(2)
winch.stop_winch()
time.sleep(1)
print("Stopped winch")
winch.raise_winch()
print("Raising winch...")