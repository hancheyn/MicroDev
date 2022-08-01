import unittest
import View
import time

def viewTest(view, detailed_array, pass_array):	
	
	view.setStandbyScreen()
	time.sleep(5)

	view.setStartScreen()
	time.sleep(5)

	view.setFlashScreen()
	time.sleep(5)

	view.setResultsScreen(pass_array)
	time.sleep(5)
	
	for i in range(0, 101):
		view.setRunningScreen(int(i))
		
	for i in range(10, 81):
		view.setRunningScreen(int(i))

	view.setDetailTestScreen(detailed_array)

	view.setSaveScreen()
	time.sleep(5)

	view.setShutdownScreen()
	time.sleep(5)

	view.setRemovalScreen()
	time.sleep(5)


view = View

detailed_array = []
for i in range(0, 60):
	detailed_array.append("Test entry: " + str(i))

pass_array = []
for i in range(0, 5):
	pass_array.append("Test entry: " + str(i))
	
viewTest(view, detailed_array, pass_array)