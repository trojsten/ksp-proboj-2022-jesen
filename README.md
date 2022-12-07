# Pravidlá
Hra sa hrá sa na mriežke políčok. \
Každé políčko je buď okysličené alebo nie. \
Kyslík sa od jeho zdroja šíri lineárne na všetky strany. \
Každý hráč má kontrolu nad niekoľkými lemurmi. V každom kroku dáva každému lemurovi príkaz, čo má robiť. \
Ak sa lemur nachádza na políčku bez kyslíka po viac ako 3 ťahy umiera. \
Každý lemur má inventár na suroviny a dva nástroje. \
Lemur vie z dostupných surovín stavať budovy a vyrábať nástroje. \
Suroviny sa získavajú ťažením. \
Pohybovať a stavať budovy sa dá len na prázdne políčko. \
Na mape sa nachádzajú aj lemury dalších hráčov.

## Ako získam kyslík ?
<<<<<<< Updated upstream
Hru začínam vo svojom "domčeku", s aspoň jedným stromom a turbínou, ktorá má v sebe citróny a teda generuje kyslík. Aby mi však všetci lemury neumreli, musím do turbíny nosiť citróny. 
Ak si vyrobím Juicer viem sa vydať aj do neokysličeného prostredia, a ak mám dostatok citorónov v inventári Juicer vždy jeden zoberie a kyslík vygeneruje.
=======
Hru začínam vo svojom "domčeku", s aspoň jedným stromom a turbínou, ktorá má v sebe citróny a teda generuje kyslík. Aby mi však všetci lemury neumreli musím do turbíny nosiť citróny. Ak si vyrobím Juicer viem sa vydať aj do neokysličeného prostredia, ak mám dostatok citorónov v inventári Juicer vždy jeden zoberie a kyslík vygeneruje.
>>>>>>> Stashed changes

### Koľko mi citrón v turbíne vydrží?
Turbína vie z jedného citrónu generovať kyslík po dobu 10 kôl.


## Zoznam príkazov
|príkaz   	|parametre   	|popis   	|
|---	|---	|---	|
|NOOP   	|-   	|Neurobí nič.   	|
|MOVE   	|(x, y)   	|Súradnice musia susediť hranou s mojou polohou. Súradnice sú absolútne.   	|
|TAKE   	|(x, y, item, quantity)   	|Vyberieš z turbníny item. Item musí byť LEMON. Súradnice musia susediť hranou s mojou polohou.   	|
|PUT   	|(x, y, item, quantity)   	| Dáš lemurovi / turbíne item. Item je jeden z InventorySlot. (Pri turbíne iba LEMON). Súradnice musia susediť hranou s mojou polohou.   	|
|BUILD   	|(x, y, tile)   	|Postavíš tile na x, y. Potrebuješ PICKAXE.  Súradnice musia susediť hranou s mojou polohou. Tile je TileType.   	|
|BREAK  	|(x, y)   	|Zbúraš tile na x, y. Potrebuješ PICKAXE. Súradnice musia susediť hranou s mojou polohou.   	|
|CRAFT  	|(tool)   	|Vyrobíš nástroj. Tool je Tool.   	|
|DISCARD   	|(item, quantity)   	| Zahodíš item. Item je jeden z InventorySlot.   	|
|STAB   	|(x, y)   	|Zabiješ lemura na x, y. Potrebuješ KNIFE. Súradnice musia susediť hranou s mojou polohou.   	|
|BONK   	|(x, y)   	|Stunneš lemura na x, y. Potrebuješ STICK. Súradnice môžu byť v okolí 5x5 okolo mňa   	|

## Zoznam surovín
|surovina   	|ako ju získam   	|
|---	|---	|
|Lemon   	|TAKE-nem zo stromu   	|
|Stone   	|BREAK-nem kameň   	|
|Iron   	|BREAK-nem železo   	|

## Zoznam nástrojov
|nástroj   	|cena   	|popis   	|
|---	|---	|---	|
|Juicer   	|3x Stone  	|ak lemur stojí na neokysličenom políčku, vytvorí z LEMON kyslík.   	|
|Pickaxe   	|2x Stone   	|umožňuje stavanie a ťaženie   	|
|Knife   	|1x Iron   	|**happy stabbing noises** umožnuje zabiť susedného lemura  	|
|Stick   	|5x Iron   	|umožnuje stunnúť lemura   	|

## Zoznam budov
|názov   	|cena   	|popis   	|
|---	|---	|---	|
|Turbine   	|20x Stone, 1x Iron   	|Po prinesení citrónu generuje kyslík.   	|
|Tree   	|5x Stone   	|Rastú na ňom citróny.   	|
|Wall   	|2x Stone   	|Stena...   	|

## Konstaty - SUBJECT TO CHANGE