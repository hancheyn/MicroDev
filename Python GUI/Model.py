#
#
#


class Model:

    view = None
    driver = None

    def __init__(self):
        print("init")
        return self

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
        return None





