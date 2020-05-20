"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   20.05.2020 12:34
"""
from ui.command_interface import Command


class UndoCommand(Command):

    def __init__(self, gm, care_taker):
        self.__gm = gm
        self.__care_taker = care_taker

    def __print_format_table(self, gm):
        print("TABLE: ")
        print(gm)

    def execute(self):
        self.__care_taker.undo()
        self.__print_format_table(self.__gm)
        while True:
            try:
                cmd = input("Do you want to do more undo [n (no), y (yes)]: ")
                if cmd != 'n' and cmd != 'y':
                    raise ValueError
                if cmd == 'n':
                    print("Adas")
                    return
                else:
                    self.__care_taker.undo()
                    self.__print_format_table(self.__gm)
            except ValueError:
                print("Invalid command, valid commands are [n (no more undo), y (more undo)]")

    def __str__(self):
        return "Undo"
