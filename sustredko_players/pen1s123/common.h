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
    ENEMY,
    OBSADENE,
    ALLY,
};

struct Tile {
    TileType type;
    int lemon = 0;

    friend std::ostream &operator<<(std::ostream &out, const Tile &t);
};

struct TurbineTile : Tile {
    explicit TurbineTile(int lemon) : Tile{TileType::TURBINE, lemon} {};

    friend std::ostream &operator<<(std::ostream &out, const TurbineTile &t);
};

struct TreeTile : Tile {
    explicit TreeTile(bool lemon) : Tile{TileType::TREE, lemon} {};

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
    int x = 0, y = 0;
    TileType tile = TileType::UNKNOWN;
    InventorySlot item = InventorySlot::LEMON;
    int quantity = 0;
    Tool tool = Tool::NO_TOOL;
};

struct NOOP : Command {
    NOOP() : Command{CommandType::NOOP} {};
};

struct STAB : Command {
    STAB(int x, int y) : Command{CommandType::STAB, x, y} {};
};

struct BONK : Command {
    BONK(int x, int y) : Command{CommandType::BONK, x, y} {};
};

struct BUILD : Command {
    BUILD(int x, int y, TileType tile) : Command{CommandType::BUILD, x, y, tile} {};
};

struct BREAK : Command {
    BREAK(int x, int y) : Command{CommandType::BREAK, x, y} {};
};

struct DISCARD : Command {
    DISCARD(InventorySlot item, int quantity) : Command{CommandType::DISCARD} {
        this->item = item;
        this->quantity = quantity;
    };
};

struct PUT : Command {
    PUT(int x, int y, InventorySlot item, int quantity) : Command{CommandType::PUT, x, y} {
        this->item = item;
        this->quantity = quantity;
    }
};

struct TAKE : Command {
    TAKE(int x, int y, InventorySlot item, int quantity) : Command{CommandType::TAKE, x, y} {
        this->item = item;
        this->quantity = quantity;
    }
};

struct CRAFT : Command {
    explicit CRAFT(Tool tool) : Command{CommandType::CRAFT} {
        this->tool = tool;
    };
};

struct MOVE : Command {
    MOVE(int x, int y) : Command{CommandType::MOVE, x, y} {};
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

std::ostream &operator<<(std::ostream &out, const Command &cmd);

std::ostream &operator<<(std::ostream &out, const CommandType &cmd);

std::ostream &operator<<(std::ostream &out, const InventorySlot &i);

std::ostream &operator<<(std::ostream &out, const Tool &t);

std::istream &operator>>(std::istream &in, Tool &t);

std::ostream &operator<<(std::ostream &out, const TileType &t);

std::istream &operator>>(std::istream &in, TileType &t);


void greet_server(const char *name, const char *color);

void send_commands(const std::vector<Command> &cmd);

#endif
