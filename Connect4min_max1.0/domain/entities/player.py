"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   12/17/2017 16:53
"""
class Player(object):
    '''
    Class for Player entity
    '''
    def __init__(self, type):
        self.__type = type
        self.__is_turn = None

    def get_type(self):
        return self.__type

    def get_turn(self):
        return self.__is_turn

    def set_turn(self, new_turn):
        self.__is_turn = new_turn