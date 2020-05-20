"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   19.05.2020 17:46
"""
from ui.close_command import CloseCommand
from ui.start_new_game_command import StartNewGameCommand


class UI:

    def __init__(self):
        self.__cmds = {
            "x": CloseCommand(),
            "1": StartNewGameCommand()
        }

    def __print_menu(self):
        print(
            "1. Start a new game\n"
            "x. Exit\n"
        )

    def __read_cmd(self):
        while True:
            try:
                cmd = input("Please give a command: ")
                if len(cmd) > 1 or len(cmd) < 1:
                    raise ValueError
                elif cmd == "x" or cmd == "1":
                    return cmd
                else:
                    raise ValueError
            except ValueError:
                print(f"Valid commands are: {list(map(str, list(self.__cmds.values())))}")

    def show_ui(self):
        while True:
            self.__print_menu()
            cmd = self.__read_cmd()
            self.__cmds[cmd].execute()
