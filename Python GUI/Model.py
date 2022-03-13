#
#
#
from time import sleep


class Model:
    view = None
    driver = None

    def __init__(self):
        print("init")

    #
    def init_model(self, view, driver):
        print("model")
        self.view = view
        self.driver = driver
        return None

    #
    def wait_model(self):
        print("wait")
        self
        return None

    #
    def display_model(self):
        print("display")
        self
        return None


# MAIN LOOP
from Controller import *
from View import *

controller = Controller
view = View
model = Model

# Initialize
driver = None
controller.controller_init(controller, model, view, driver)
model.init_model(model, view, driver)

while True:
    print("1")
    sleep(1)
