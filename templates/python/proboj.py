import enum
import sys


class Command(enum.Enum):
    """
    Reprezentuje typ príkazov.

    * NOOP() - Neurobí nič
    * STAB(x, y) - Zabiješ lemura na x, y.
        Potrebuješ KNIFE.
        Súradnice musia susediť hranou s mojou polohou.
    * BONK(x, y) - Stunneš lemura na x, y.
        Potrebuješ STICK.
        Súradnice môžu byť v okolí 5x5 okolo mňa.
    * BUILD(x, y, tile) - Postavíš tile na x, y.
        Potrebuješ PICKAXE.
        Súradnice musia susediť hranou s mojou polohou.
        Tile je TileType.
    * BREAK(x, y) - Zbúraš tile na x, y.
        Potrebuješ PICKAXE.
        Súradnice musia susediť hranou s mojou polohou.
    * DISCARD(item, quantity) - Zahodíš item.
        Item je jeden z InventorySlot.
    * PUT(x, y, item, quantity) - Dáš lemurovi / turbíne item.
        Item je jeden z InventorySlot. (Pri turbíne iba LEMON)
        Súradnice musia susediť hranou s mojou polohou.
    * TAKE(x, y, item, quantity) - Vyberieš z turbníny item.
        Item je LEMON.
        Súradnice musia susediť hranou s mojou polohou.
    * CRAFT(tool) - Vyrobíš nástroj.
        Tool je Tool.
    * MOVE(x, y) - Presunieš sa na x, y.
        Súradnice musia susediť hranou s mojou polohou.
        Súradnice sú absolútne.
    """
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
    """
    Reprezentuje nástroj.

    * JUICER - ak je lemur bez kyslíka a má LEMON,
        minie LEMON a vytvára kyslík
    * PICKAXE - lemur vie stavať a búrať
    * KNIFE - lemur môže zabiť iného
    * STICK - lemur môže stunnúť iného
    """
    JUICER = 0
    PICKAXE = 1
    KNIFE = 2
    STICK = 3
    NO_TOOL = 4


class InventorySlot(enum.Enum):
    """
    Reprezentuje slot inventára.
    """
    LEMON = 0
    STONE = 1
    IRON = 2
    TOOL1 = 3
    TOOL2 = 4


class TileType(enum.Enum):
    """
    Reprezentuje druhy políčok.
    """
    EMPTY = 0
    STONE = 1
    IRON = 2
    TREE = 3
    TURBINE = 4
    WALL = 5
    UNKNOWN = 6


class Tile:
    """
    Reprezentuje políčko.

    * type - TileType tohto políčka
    """
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
    """
    Reprezentuje turbínu.
    Turbína produkuje kyslík, kým má dostatok LEMONov, ktoré
    možno priávať commandom PUT.

    * type - TileType tohto políčka (TURBINE)
    * lemon - počet LEMONov v turbíne
    """
    def __init__(self, lemon: int):
        super().__init__(TileType.TURBINE)
        self.lemon = lemon


class TreeTile(Tile):
    """
    Reprezentuje citrónovník.
    Na citrónovníku rastú LEMONy, ktoré sa dajú zbierať pomocou
    commandu TAKE. Na citrónovníku vie byť najviac jeden LEMON.

    * type - TileType tohto políčka (TREE)
    * has_lemon - má tento strom LEMON?
    """
    def __init__(self, lemon: bool):
        super().__init__(TileType.TREE)
        self.has_lemon = lemon


class World:
    """
    Reprezentuje svet.

    * width - sirka
    * height - vyska
    * tiles - pole [y][x] objektov Tile
    * oxygen - pole [y][x] intov s hodnotami kyslíka
    """
    def __init__(self):
        self.width: int = 0
        self.height: int = 0
        self.tiles: list[list[Tile]] = []
        self.oxygen: list[list[int]] = []

    def read_world(self):
        """
        Prečíta sekciu 1 zo stavu
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
        Prečíta sekciu 3 zo stavu
        """
        if not self.oxygen:
            self.oxygen = [[0] * self.width for _ in range(self.height)]

        for y in range(self.height):
            self.oxygen[y] = list(map(int, input().split()))


class Lemur:
    """
    Reprezentuje lemura.

    * alive - je živý?
    * x, y - súradnice
    * iron - počet IRONu v inventári
    * lemon - počet LEMONov v inventári
    * stone - počet STONEov v inventári
    * stunned - počet ťahov, ktoré je lemur stunnutý
    * tools - pole s Tool
    """
    def __init__(self):
        self.alive: bool = True
        self.x: int = 0
        self.y: int = 0
        self.iron: int = 0
        self.lemon: int = 0
        self.stone: int = 0
        self.stunned: int = 0
        self.tools: list[Tool | None] = []

    def read_lemur(self):
        """
        Prečíta lemura zo stavu hry.
        """
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
        self.stunned = data[6]
        self.tools = []
        for t in data[7:]:
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
    """
    Reprezentuje ťah konkrétneho lemura.
    """
    def __init__(self, command: Command, *args: int|enum.Enum):
        self.command = command
        self.args = args

    def print(self):
        """
        Vypíše ťah serveru.
        """
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
    """
    Reprezentuje hráča v hre.

    * idx - jeho číslo v poli hráčov
    * lemurs - pole objektov Lemur
        Pole má konštantnú veľkosť, mŕtvy lemuri v ňom zostávajú.
        Poradie lemurov sa počas hry nemení.
    * alive - má hráč aspoň jedného živého lemura?
    """
    def __init__(self, idx: int):
        self.idx = idx
        self.lemurs: list[Lemur] = []

    def read_lemurs(self):
        """
        Prečíta lemurov zo stavu hry.
        """
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
    """
    Reprezentuje nášho klienta.

    * world - objekt World
    * players - pole objektov Player
    * myself - môj hráč v poli players
    """
    def __init__(self):
        self.world = World()
        self.players: list[Player] = []
        self._myself: int = 0

    @property
    def myself(self) -> Player:
        """
        Vráti môjho Player.
        """
        return self.players[self._myself]

    def log(self, *args):
        """
        Vypíše dáta do logu. Syntax je rovnaká ako print().
        """
        print(*args, file=sys.stderr)

    def get_color(self) -> str:
        """
        Farba hráča v hexadecimálnom tvare bez # na začiatku.
        """
        raise NotImplementedError()

    def get_name(self) -> str:
        """
        Meno hráča, ktoré sa zobrazí v observeri.
        """
        raise NotImplementedError()

    def _greet(self):
        """
        Spracuje HELLO od serveru.
        """
        gr = input()
        input()
        assert gr == "HELLO"
        print(self.get_name(), self.get_color())
        print(".")

    def _read_players(self):
        """
        Prečíta 2 sekciu stavu hry.
        """
        player_count, myself = map(int, input().split())
        self._myself = myself
        if not self.players:
            self.players = [Player(i) for i in range(player_count)]

        for i in range(player_count):
            self.players[i].read_lemurs()

    def _read_turn(self):
        """
        Prečíta celý stav.
        """
        self.world.read_world()
        self._read_players()
        self.world.read_oxygen()
        input()
        input()

    def _send_turns(self, turns: list[Turn]):
        """
        Odošle ťahy serveru.
        """
        for t in turns:
            t.print()
        print(".")

    def make_turn(self) -> list[Turn]:
        """
        Vykoná ťah.
        Funkcia vracia pole objektov Turn, jeden pre každého lemura.
        """
        raise NotImplementedError()

    def run(self):
        """
        Hlavný cyklus hry.
        """
        self._greet()
        while True:
            self._read_turn()
            turns = self.make_turn()
            self._send_turns(turns)
