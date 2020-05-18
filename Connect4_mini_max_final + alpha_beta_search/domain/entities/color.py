"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   12/17/2017 19:07
"""


class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

    def __init__(self, type):
        self.__type = type

    def get_color(self):
        if self.__type == 1:
            return self.BLUE
        elif self.__type == 2:
            return self.RED
        else:
            return self.BOLD

    def get_end_clr(self):
        return self.END
