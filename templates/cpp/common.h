#ifndef COMMON_H
#define COMMON_H

#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <ranges>
#include <iterator>
#include <sstream>

enum class CommandType : int {
    NOOP,
    STAB,
    BONK,
    BUILD,
    BREAK,
    DISCARD,
    PUT,
    TAKE,
    CRAFT,
    MOVE,
};

enum class InventorySlot : int {
    LEMON,
    STONE,
    IRON,
    TOOL1,
    TOOL2,
};

enum class Tool : int {
    JUICER,
    PICKAXE,
    KNIFE,
    STICK,
    NO_TOOL,
};

enum class TileType : int {
    EMPTY,
    STONE,
    IRON,
    TREE,
    TURBINE,
    WALL,
    UNKNOWN,
};

struct Tile {
    TileType type;

    friend std::ostream &operator<<(std::ostream &out, const Tile &t);
};

struct TurbineTile : Tile {
    int lemon;

    explicit TurbineTile(int lemon) : Tile{TileType::TURBINE}, lemon(lemon) {};

    friend std::ostream &operator<<(std::ostream &out, const TurbineTile &t);
};

struct TreeTile : Tile {
    bool has_lemon;

    explicit TreeTile(bool lemon) : Tile{TileType::TREE}, has_lemon(lemon) {};

    friend std::ostream &operator<<(std::ostream &out, const TreeTile &t);
};

struct Lemur {
    bool alive = true, is_stunned = false;
    int x = 0, y = 0, iron = 0, lemon = 0, stone = 0;
    std::vector<Tool> tools;

    friend std::istream &operator>>(std::istream &in, Lemur &l);

    friend std::ostream &operator<<(std::ostream &out, const Lemur &l);
};

struct Player {
    int id;
    std::vector<Lemur> lemurs;
    bool alive = false;

    Player() {
        id = _id++;
    }

    friend std::istream &operator>>(std::istream &in, Player &p);

    friend std::ostream &operator<<(std::ostream &out, const Player &p);

private:
    static int _id;
};


struct World {
    int width = 0;
    int height = 0;
    int my_id = 0;
    std::vector<std::vector<Tile>> tiles;
    std::vector<Player> players;
    std::vector<std::vector<int>> oxygen;

    friend std::istream &operator>>(std::istream &in, World &w);

    friend std::ostream &operator<<(std::ostream &out, const World &w);
};

struct Command {
    CommandType type;
};

struct NOOP : Command {
    NOOP() : Command{CommandType::NOOP} {};
};

struct STAB : Command {
    int x, y;

    STAB(int x, int y) : Command{CommandType::STAB}, x(x), y(y) {};
};

struct BONK : Command {
    int x, y;

    BONK(int x, int y) : Command{CommandType::BONK}, x(x), y(y) {};
};

struct BUILD : Command {
    int x, y;
    TileType tile;

    BUILD(int x, int y, TileType tile) :
            Command{CommandType::BUILD},
            x(x),
            y(y),
            tile(tile) {};
};

struct BREAK : Command {
    int x, y;

    BREAK(int x, int y) : Command{CommandType::BREAK}, x(x), y(y) {};
};

struct DISCARD : Command {
    InventorySlot item;
    int quantity;

    DISCARD(InventorySlot item, int quantity) :
            Command{CommandType::DISCARD},
            item(item),
            quantity(quantity) {};
};

struct PUT : Command {
    int x, y;
    InventorySlot item;
    int quantity;

    PUT(int x, int y, InventorySlot item, int quantity) :
            Command{CommandType::PUT},
            x(x),
            y(y),
            item(item),
            quantity(quantity) {};
};

struct TAKE : Command {
    int x, y;
    InventorySlot item;
    int quantity;

    TAKE(int x, int y, InventorySlot item, int quantity) :
            Command{CommandType::TAKE},
            x(x),
            y(y),
            item(item),
            quantity(quantity) {};
};

struct CRAFT : Command {
    Tool tool;

    explicit CRAFT(Tool tool) : Command{CommandType::CRAFT}, tool(tool) {};
};

struct MOVE : Command {
    int x, y;

    MOVE(int x, int y) : Command{CommandType::MOVE}, x(x), y(y) {};
};

/**
* Print any vector to output
* @tparam T type inside vector
* @param out stream to which output will we written
* @param v input vector
* @return out stream
*/
namespace std {
    template<class T>
    ostream &operator<<(ostream &out, const vector<T> &v) {
        ranges::copy(v, ostream_iterator<T>(out, " "));
        out << '\n';
        return out;
    }
}

std::ostream &operator<<(std::ostream &out, const CommandType &cmd);

std::ostream &operator<<(std::ostream &out, const InventorySlot &i);

std::ostream &operator<<(std::ostream &out, const Tool &t);

std::istream &operator>>(std::istream &in, Tool &t);

std::ostream &operator<<(std::ostream &out, const TileType &t);

std::istream &operator>>(std::istream &in, TileType &t);


void greet_server(const char *name, const char *color);

void send_commands(const std::vector<Command> &cmd);

#endif
