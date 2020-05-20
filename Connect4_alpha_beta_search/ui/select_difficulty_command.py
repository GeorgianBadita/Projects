"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   20.05.2020 12:44
"""
from ui.command_interface import Command
from utils import settings


class SelectDifficultyCommand(Command):

    def __print_menu(self):
        print(
            "1. EASY\n"
            "2. MEDIUM\n"
            "3. HARD\n"
        )

    def __read_command(self):
        while True:
            try:
                cmd = int(input("Please select a difficulty: "))
                if cmd != 1 and cmd != 2 and cmd != 3:
                    raise ValueError
                return cmd
            except ValueError:
                print("Valid commands: [1 - EASY, 2 - MEDIUM, 3 - HARD]")

    def execute(self):
        self.__print_menu()
        cmd = self.__read_command()
        settings.DEPTH = 2 * cmd + 1

    def __str__(self):
        return "Select difficulty"
