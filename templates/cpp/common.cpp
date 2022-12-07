#include "common.h"

//uplne nezaujimave nemusis citat
//definuje iba format komunikacie so serverom

std::istream &operator>>(std::istream &in, TileType &t) {
    int a;
    in >> a;
    t = static_cast<TileType>(a);
    return in;
}

std::ostream &operator<<(std::ostream &out, const CommandType &cmd) {
    std::vector<std::string> mapping{
            "NOOP",
            "STAB",
            "BONK",
            "BUILD",
            "BREAK",
            "DISCARD",
            "PUT",
            "TAKE",
            "CRAFT",
            "MOVE",
    };
    out << mapping[static_cast<int>(cmd)];
    return out;
}

std::ostream &operator<<(std::ostream &out, const Tool &t) {
    std::vector<std::string> mapping{
            "JUICER",
            "PICKAXE",
            "KNIFE",
            "STICK",
            "NO_TOOL",
    };
    out << mapping[static_cast<int>(t)];
    return out;
}

std::istream &operator>>(std::istream &in, Tool &t) {
    int a;
    in >> a;
    t = static_cast<Tool>(a);
    return in;
}

std::ostream &operator<<(std::ostream &out, const InventorySlot &i) {
    out << static_cast<int>(i);
    return out;
}

std::ostream &operator<<(std::ostream &out, const TileType &t) {
    std::vector<std::string> mapping{
            "EMPTY",
            "STONE",
            "IRON",
            "TREE",
            "TURBINE",
            "WALL",
            "UNKNOWN",
    };
    out << mapping[static_cast<int>(t)];
    return out;
}

std::ostream &operator<<(std::ostream &out, const Command &cmd) {
    out << cmd.type;
    switch (cmd.type) {
        case CommandType::NOOP:
            break;
        case CommandType::STAB:
            out << " " << static_cast<const STAB &>(cmd).x;
            out << " " << static_cast<const STAB &>(cmd).y;
            break;
        case CommandType::BONK:
            out << " " << static_cast<const BONK &>(cmd).x;
            out << " " << static_cast<const BONK &>(cmd).y;
            break;
        case CommandType::BUILD:
            out << " " << static_cast<const BUILD &>(cmd).x;
            out << " " << static_cast<const BUILD &>(cmd).y;
            out << " " << static_cast<const BUILD &>(cmd).tile;
            break;
        case CommandType::BREAK:
            out << " " << static_cast<const BREAK &>(cmd).x;
            out << " " << static_cast<const BREAK &>(cmd).y;
            break;
        case CommandType::DISCARD:
            out << " " << static_cast<const DISCARD &>(cmd).item;
            out << " " << static_cast<const DISCARD &>(cmd).quantity;
            break;
        case CommandType::PUT:
            out << " " << static_cast<const PUT &>(cmd).x;
            out << " " << static_cast<const PUT &>(cmd).y;
            out << " " << static_cast<const PUT &>(cmd).item;
            out << " " << static_cast<const PUT &>(cmd).quantity;
            break;
        case CommandType::TAKE:
            out << " " << static_cast<const TAKE &>(cmd).x;
            out << " " << static_cast<const TAKE &>(cmd).y;
            out << " " << static_cast<const TAKE &>(cmd).item;
            out << " " << static_cast<const TAKE &>(cmd).quantity;
            break;
        case CommandType::CRAFT:
            out << " " << static_cast<int>(static_cast<const CRAFT &>(cmd).tool);
            break;
        case CommandType::MOVE:
            out << " " << static_cast<const MOVE &>(cmd).x;
            out << " " << static_cast<const MOVE &>(cmd).y;
            break;
    }
    return out;
}

void greet_server(const char *name, const char *color) {
    std::string hello;
    char dot;
    std::cin >> hello >> dot;
    std::cout << name << ' ' << color << "\n." << std::endl;
}

void send_commands(const std::vector<Command> &commands) {
    std::ranges::copy(commands, std::ostream_iterator<Command>(std::cout, "\n"));
    std::cout << '.' << std::endl;
}

int Player::_id = 0;

std::istream &operator>>(std::istream &in, Player &p) {
    int lemurs_count;
    in >> lemurs_count;
    p.lemurs.resize(lemurs_count);

    p.alive = false;

    for (int i = 0; i < lemurs_count; i++) {
        in >> p.lemurs[i];
        if (p.lemurs[i].alive) p.alive = true;
    }

    return in;
}

std::ostream &operator<<(std::ostream &out, const Player &p) {
    if (p.alive) out << "alive";
    else out << "dead ";
    out << " player" << p.id << " lemurs: " << p.lemurs;
    return out;
}

std::ostream &operator<<(std::ostream &out, const Tile &t) {
    out << t.type;
    return out;
}

std::ostream &operator<<(std::ostream &out, const TurbineTile &t) {
    out << static_cast<Tile>(t) << " " << t.lemon;
    return out;
}

std::ostream &operator<<(std::ostream &out, const TreeTile &t) {
    out << static_cast<Tile>(t) << " " << t.has_lemon;
    return out;
}

std::istream &operator>>(std::istream &in, Lemur &l) {
    in >> l.alive;
    if (l.alive) {
        in >> l.x >> l.y >> l.iron >> l.lemon >> l.stone >> l.is_stunned;
        std::string line;
        std::getline(in, line);
        std::istringstream line_in{line};
        unsigned int i = 0;
        for (Tool t; line_in >> t; i++) {
            if (i < l.tools.size()) {
                l.tools[i] = t;
            } else {
                l.tools.push_back(t);
            }
        }
        if (i < l.tools.size()) l.tools.resize(i);
    }
    return in;
}

std::ostream &operator<<(std::ostream &out, const Lemur &l) {
    out << l.alive << " x: " << l.x << ", y: " << l.y << ", iron: " << l.iron;
    out << ", lemon: " << l.lemon << ", stone: " << l.stone;
    out << ", stunned: " << l.is_stunned << ", tools: " << l.tools;
    return out;
}

std::istream &operator>>(std::istream &in, World &w) {
    in >> w.width >> w.height;

    w.tiles.resize(w.height, std::vector<Tile>(w.width, {TileType::UNKNOWN}));

    for (int i = 0; i < w.height; i++) {
        for (int j = 0; j < w.width; j++) {
            TileType t;
            in >> t;
            switch (t) {
                case TileType::TURBINE:
                    int lemon;
                    in >> lemon;
                    w.tiles[i][j] = TurbineTile{lemon};
                    break;
                case TileType::TREE:
                    bool has_lemon;
                    in >> has_lemon;
                    w.tiles[i][j] = TreeTile{has_lemon};
                    break;
                default:
                    w.tiles[i][j] = {t};
            }
        }
    }

    int player_count;
    in >> player_count >> w.my_id;

    w.players.resize(player_count);

    for (int i = 0; i < player_count; i++) in >> w.players[i];

    w.oxygen.resize(w.height, std::vector<int>(w.width, 0));

    for (int i = 0; i < w.height; i++)
        for (int j = 0; j < w.width; j++)
            in >> w.oxygen[i][j];

    char dot;
    std::cin >> dot;
    return in;
}

std::ostream &operator<<(std::ostream &out, const World &w) {
    out << w.width << " " << w.height << '\n';
    out << w.tiles << w.players << w.oxygen;
    return out;
}
