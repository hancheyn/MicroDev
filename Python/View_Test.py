import unittest
import View
import time


view = View
pass_array = ["h", "e", "l", "l", "o"]
detailed_array = ["Hello World"]

view.setStandbyScreen()
time.sleep(1)
view.setStartScreen()
time.sleep(1)
view.setFlashScreen()
time.sleep(1)
view.setRunningScreen(pass_array)
time.sleep(1)
view.setResultsScreen(pass_array)
time.sleep(1)
view.setDetailTestScreen(detailed_array)
time.sleep(1)
view.setSaveScreen()
time.sleep(1)
view.setShutdownScreen()
time.sleep(1)
view.setRemovalScreen()
