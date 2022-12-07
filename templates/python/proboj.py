import enum
import sys


class Command(enum.Enum):
    NOOP = "NOOP"
    STAB = "STAB"
    BONK = "BONK"
    BUILD = "BUILD"
    BREAK = "BREAK"
    DISCARD = "DISCARD"
    PUT = "PUT"
    TAKE = "TAKE"
    CRAFT = "CRAFT"
    MOVE = "MOVE"


class Tool(enum.Enum):
    JUICER = 0
    PICKAXE = 1
    KNIFE = 2
    STICK = 3
    NO_TOOL = 4


class InventorySlot(enum.Enum):
    LEMON = 0
    STONE = 1
    IRON = 2
    TOOL1 = 3
    TOOL2 = 4


class TileType(enum.Enum):
    EMPTY = 0
    STONE = 1
    IRON = 2
    TREE = 3
    TURBINE = 4
    WALL = 5
    UNKNOWN = 6


class Tile:
    def __init__(self, type: TileType):
        self.type = type

    @classmethod
    def from_state(cls, state: list[int]) -> "Tile":
        typ = TileType(state.pop(0))
        if typ == TileType.TURBINE:
            return TurbineTile(state.pop(0))
        if typ == TileType.TREE:
            return TreeTile(bool(state.pop(0)))
        return Tile(typ)


class TurbineTile(Tile):
    def __init__(self, lemon: int):
        super().__init__(TileType.TURBINE)
        self.lemon = lemon


class TreeTile(Tile):
    def __init__(self, lemon: bool):
        super().__init__(TileType.TREE)
        self.has_lemon = lemon


class World:
    def __init__(self):
        self.width: int = 0
        self.height: int = 0
        self.tiles: list[list[Tile]] = []
        self.oxygen: list[list[int]] = []

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

    def read_oxygen(self):
        """
        Reads section 3 (lighting data) of the state
        """
        if not self.oxygen:
            self.oxygen = [[0] * self.width for _ in range(self.height)]

        for y in range(self.height):
            self.oxygen[y] = list(map(int, input().split()))


class Lemur:
    def __init__(self):
        self.alive: bool = True
        self.x: int = 0
        self.y: int = 0
        self.iron: int = 0
        self.lemon: int = 0
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
        self.iron = data[3]
        self.lemon = data[4]
        self.stone = data[5]
        self.tools = []
        for t in data[6:]:
            tool = Tool(t)
            if tool == Tool.NO_TOOL:
                self.tools.append(None)
            else:
                self.tools.append(tool)
    
    def tool_index(self, tool):
        for i in range(len(self.tools)):
            if self.tools[i]==tool:
                return i
        return None
    
    def have_tool(self, tool):
        return self.tool_index(tool) is not None


class Turn:
    def __init__(self, command: Command, *args: int):
        self.command = command
        self.args = args

    def print(self):
        args = []
        for a in self.args:
            if isinstance(a, enum.Enum):
                a = a.value
            if isinstance(a, int):
                args.append(a)
            else:
                raise ValueError(f"Invalid argument type: {type(a)}")
        print(self.command.value, *map(int, args))


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
        input()
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
        self.world.read_oxygen()
        input()
        input()

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
