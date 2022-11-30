import enum
import sys


class Command(enum.StrEnum):
    NOOP = "NOOP"
    STAB = "STAB"
    SHOOT = "SHOOT"
    BUILD = "BUILD"
    BREAK = "BREAK"
    DISCARD = "DISCARD"
    PUT = "PUT"
    TAKE = "TAKE"
    CRAFT = "CRAFT"
    MOVE = "MOVE"
    MIRROR = "MIRROR"


class Tool(enum.IntEnum):
    LANTERN = 0
    PICKAXE = 1
    HAMMER = 2
    KNIFE = 3
    MIRROR = 4
    GUN = 5
    NO_TOOL = 6


class TileType(enum.IntEnum):
    EMPTY = 0
    STONE = 1
    GOLD = 2
    COAL = 3
    TREE = 4
    FURNACE = 5
    TRAP = 6
    CHEST = 7
    UNKNOWN = 8


class Tile:
    def __init__(self, type: TileType):
        self.type = type

    @classmethod
    def from_state(cls, state: list[int]) -> "Tile":
        typ = TileType(state.pop(0))
        if typ == TileType.CHEST:
            return ChestTile(state.pop(0), state.pop(0), state.pop(0), state.pop(0))
        if typ == TileType.FURNACE:
            return FurnaceTile(state.pop(0))
        if typ == TileType.TREE:
            return TreeTile(bool(state.pop(0)))
        return Tile(typ)


class ChestTile(Tile):
    def __init__(self, cocos: int, gold: int, coal: int, stone: int):
        super().__init__(TileType.CHEST)
        self.cocos = cocos
        self.gold = gold
        self.coal = coal
        self.stone = stone


class FurnaceTile(Tile):
    def __init__(self, coal: int):
        super().__init__(TileType.FURNACE)
        self.coal = coal


class TreeTile(Tile):
    def __init__(self, cocos: bool):
        super().__init__(TileType.FURNACE)
        self.has_cocos = cocos


class World:
    def __init__(self):
        self.width: int = 0
        self.height: int = 0
        self.tiles: list[list[Tile]] = []
        self.light: list[list[int]] = []

    def read_world(self):
        """
        Reads section 1 (world data) of the state
        """
        self.width, self.height = map(int, input().split())
        self.tiles = [
            [Tile(TileType.UNKNOWN) for _ in range(self.width)]
            for _ in range(self.height)
        ]

        for y in range(self.height):
            state = list(map(int, input().split()))
            for x in range(self.width):
                self.tiles[y][x] = Tile.from_state(state)

    def read_light(self):
        """
        Reads section 3 (lighting data) of the state
        """
        for y in range(self.height):
            self.light[y] = list(map(int, input().split()))


class Lemur:
    def __init__(self):
        self.alive: bool = True
        self.x: int = 0
        self.y: int = 0
        self.cocos: int = 0
        self.gold: int = 0
        self.coal: int = 0
        self.stone: int = 0
        self.tools: list[Tool | None] = []

    def read_lemur(self):
        data = list(map(int, input().split()))
        if data[0] == 0:
            self.alive = False
            return

        self.alive = True
        self.x = data[1]
        self.y = data[2]
        self.cocos = data[3]
        self.gold = data[4]
        self.coal = data[5]
        self.stone = data[6]
        self.tools = []
        for t in data[7:]:
            tool = Tool(t)
            if tool == Tool.NO_TOOL:
                self.tools.append(None)
            else:
                self.tools.append(tool)


class Turn:
    def __init__(self, command: Command, *args: int):
        self.command = command
        self.args = args

    def print(self):
        print(self.command, *self.args)


class Player:
    def __init__(self, idx: int):
        self.idx = idx
        self.lemurs: list[Lemur] = []

    def read_lemurs(self):
        lemur_count = int(input())
        while len(self.lemurs) < lemur_count:
            self.lemurs.append(Lemur())

        for i in range(lemur_count):
            self.lemurs[i].read_lemur()

    @property
    def alive(self) -> bool:
        for l in self.lemurs:
            if l.alive:
                return True
        return False


class ProbojPlayer:
    def __init__(self):
        self.world = World()
        self.players: list[Player] = []
        self._myself: int = 0

    @property
    def myself(self) -> Player:
        return self.players[self._myself]

    def log(self, *args):
        print(*args, file=sys.stderr)

    def get_color(self) -> str:
        """
        Gets the hexadecimal color of the player without # prefix.
        """
        raise NotImplementedError()

    def get_name(self) -> str:
        """
        Gets the player's display name. Spaces are not allowed in the name.
        """
        raise NotImplementedError()

    def _greet(self):
        gr = input()
        assert gr == "HELLO"
        print(self.get_name(), self.get_color())
        print(".")

    def _read_players(self):
        """
        Reads section 2 (players) of the state
        """
        player_count, myself = map(int, input().split())
        self._myself = myself
        if not self.players:
            self.players = [Player(i) for i in range(player_count)]

        for i in range(player_count):
            self.players[i].read_lemurs()

    def _read_turn(self):
        self.world.read_world()
        self._read_players()
        self.world.read_light()

    def _send_turns(self, turns: list[Turn]):
        for t in turns:
            t.print()
        print(".")

    def make_turn(self) -> list[Turn]:
        raise NotImplementedError()

    def run(self):
        self._greet()
        while True:
            self._read_turn()
            turns = self.make_turn()
            self._send_turns(turns)