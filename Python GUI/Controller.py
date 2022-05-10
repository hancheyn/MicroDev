# #################################################
# MicroDev Project: Controller
# Date: May 2, 2022
# Description: Controller Class
# Authors:
# Nathan Hanchey
# Dylan
# Connor
# Corey
# #################################################

from time import sleep
import Model
import View


###################################################################################
class Controller:
    driver = None
    view = None

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
        return None

    #
    def display_model(self):
        print("display")
        self
        return None


# ###############################################################################
# MAIN LOOP
# ###############################################################################
controller = Controller
view = View
model = Model

# Initialize
driver = None
#controller.controller_init(controller, model, view, driver)
#model.init_model(model, view, driver)

while True:
    print("1")
    sleep(1)


