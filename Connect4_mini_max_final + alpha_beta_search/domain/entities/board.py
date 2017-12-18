"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   12/17/2017 16:53
"""
from domain.entities.color import Color
class Board(object):
    '''
    Class fot he board entity
    '''

    table_points = [[3, 4, 5, 7, 5, 4, 3],
                    [4, 6, 8, 10, 8, 6, 4],
                    [5, 8, 11, 13, 11, 8, 5],
                    [5, 8, 11, 13, 11, 8, 5],
                    [4, 6, 8, 10, 8, 6, 4],
                    [3, 4, 5, 7, 5, 4, 3]]



    def __init__(self, height, width):
        self.__height = height
        self.__width = width
        self.__table = [[0 for i in range(width)] for j in range(height)]

    def get_height(self):
        return self.__height

    def get_width(self):
        return self.__width

    def get_table(self):
        return self.__table

    def set_table(self, lin, col, value):
        self.__table[lin][col] = value

    def draw_board(self):
        string_board = ""
        table = self.get_table()
        for line in range(len(table)):
            for col in range(len(table[0])):
                clr_obj = Color(table[line][col])
                clr = clr_obj.get_color()
                end_clr = clr_obj.get_end_clr()
                string_board = string_board + clr + "o" + end_clr + " "
            string_board += "\n"
        print(string_board)

    def evaluate_board(self):
        """
        Function that evaluates a certain state
        of the board
        :return:
        """
        utility = 0
        sum = 0
        table = self.get_table()
        for line in range(len(table)):
            for col in range(len(table[0])):
                if table[line][col] == 2:
                    sum += self.table_points[line][col]
                elif table[line][col] == 1:
                    sum -= self.table_points[line][col]
        return utility + sum