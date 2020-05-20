"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   19.05.2020 17:52
"""
from ui.command_interface import Command


class CloseCommand(Command):

    def execute(self):
        exit()

    def __str__(self):
        return "Close"
