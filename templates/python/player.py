from proboj import *


class MyPlayer(ProbojPlayer):
    def get_color(self) -> str:
        return "042069"

    def get_name(self) -> str:
        return "Example.py"

    def make_turn(self) -> list[Turn]:
        return [Turn(Command.NOOP)]


if __name__ == "__main__":
    p = MyPlayer()
    p.run()
