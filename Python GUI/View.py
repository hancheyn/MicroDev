#
#
#
class View:
    #
    def __init__(self):
        print("view")
        return self

    #
    @staticmethod
    def update_view_debug(String):
        print("update")

        return None

    #
    @staticmethod
    def clear_view(self):
        print("clear")

        return None

    #
    @staticmethod
    def update_view_begin(self):
        print("begin")
        return None


view = View
view.clear_view(view)
