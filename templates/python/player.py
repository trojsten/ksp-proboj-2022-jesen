from .proboj import *


class MyPlayer(ProbojPlayer):
    def get_color(self) -> str:
        pass

    def get_name(self) -> str:
        pass

    def make_turn(self) -> list[Turn]:
        pass


if __name__ == "__main__":
    p = MyPlayer()
    p.run()
