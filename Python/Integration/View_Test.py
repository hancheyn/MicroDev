import unittest
import View
import time


view = View
pass_array = ["h", "e", "l", "l", "o"]
detailed_array = []
for i in range(0, 23):
	detailed_array.append("Test entry: " + str(i) + "\n")
	
view.setDetailTestScreen(detailed_array)
