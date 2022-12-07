#ifndef COMMON_H
#define COMMON_H

#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <ranges>
#include <iterator>
#include <sstream>


namespace std {
	template<class T>
	ostream& operator<< (ostream& out, const vector<T>& v) {
		ranges::copy(v, ostream_iterator<T>(out, " "));
		out << '\n';
		return out;
	}
}

enum class CommandType: int {
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

std::ostream& operator<< (std::ostream& out, const CommandType& cmd);

enum class InventorySlot: int {
	LEMON,
	STONE,
	IRON,
	TOOL1,
	TOOL2,
};

std::ostream& operator<< (std::ostream& out, const InventorySlot& i);

enum class Tool: int {
	JUICER,
	PICKAXE,
	KNIFE,
	STICK,
	NO_TOOL,
};

std::ostream& operator<< (std::ostream& out, const Tool& t);
std::istream& operator>> (std::istream& in, Tool& t);

enum class TileType: int {
	EMPTY,
	STONE,
	IRON,
	TREE,
	TURBINE,
	WALL,
	UNKNOWN,
};

std::ostream& operator<< (std::ostream& out, const TileType& t);
std::istream& operator>> (std::istream& in, TileType& t);

struct Tile {
	TileType type;
	
	friend std::ostream& operator<< (std::ostream& out, const Tile& t) {
		out << t.type;
		return out;
	}
};

struct TurbineTile: Tile {
	int lemon;
	TurbineTile(int lemon): Tile(TileType::TURBINE), lemon(lemon) {};
	
	friend std::ostream& operator<< (std::ostream& out, const TurbineTile& t) {
		out << t << " " << t.lemon;
		return out;
	}
};

struct TreeTile: Tile {
	bool has_lemon;
	TreeTile(bool lemon): Tile(TileType::TREE), has_lemon(lemon) {};
	
	friend std::ostream& operator<< (std::ostream& out, const TreeTile& t) {
		out << t << " " << t.has_lemon;
		return out;
	}
};

struct Lemur {
	bool alive = true, is_stunned = false;
	int x = 0, y = 0, iron = 0, lemon = 0, stone = 0;
	std::vector<Tool> tools;
	
	friend std::istream& operator>> (std::istream& in, Lemur& l){
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
	
	friend std::ostream& operator<< (std::ostream& out, const Lemur& l) {
		out << l.alive << " x: " << l.x << ", y: " << l.y << ", iron: " << l.iron;
		out << ", lemon: " << l.lemon << ", stone: " << l.stone;
		out << ", stunned: " << l.is_stunned <<", tools: " << l.tools;
		return out;
	}
};

struct Player {
	int id;
	std::vector<Lemur> lemurs;
	bool alive;
	
	Player () {
		id = _id++;
	}
	
	friend std::istream& operator>> (std::istream& in, Player& p){
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
	
	friend std::ostream& operator<< (std::ostream& out, const Player& p) {
		if (p.alive) out << "alive";
		else out << "dead ";
		out << " player" << p.id << " lemurs: " << p.lemurs;
		return out;
	}
	
	private:
		static int _id;
};

std::ostream& operator<< (std::ostream& out, const std::vector<Player>& v);


struct World {
	int width = 0;
	int height = 0;
	int my_id = 0;
	std::vector<std::vector<Tile>> tiles;
	std::vector<Player> players;
	std::vector<std::vector<int>> oxygen;

	friend std::istream& operator>> (std::istream& in, World& w){
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
	
	friend std::ostream& operator<< (std::ostream& out, const World& w) {
		out << w.width << " " << w.height << '\n';
		out << w.tiles << w.players << w.oxygen;
		return out;
	}
};

struct Command {
	CommandType type;
};

struct NOOP: Command {
	NOOP(): Command(CommandType::NOOP) {};
};

struct STAB: Command {
	int x, y;
	STAB(int x, int y): Command(CommandType::STAB), x(x), y(y) {};
};

struct BONK: Command {
	int x, y;
	BONK(int x, int y): Command(CommandType::BONK), x(x), y(y) {};
};

struct BUILD: Command {
	int x, y;
	TileType tile;
	BUILD(int x, int y, TileType tile):
		Command(CommandType::BUILD),
		x(x),
		y(y),
		tile(tile) {};
};

struct BREAK: Command {
	int x, y;
	BREAK(int x, int y): Command(CommandType::BREAK), x(x), y(y) {};
};

struct DISCARD: Command {
	InventorySlot item;
	int quantity;
	DISCARD(InventorySlot item, int quantity):
		Command(CommandType::DISCARD),
		item(item),
		quantity(quantity) {};
};

struct PUT: Command {
	int x, y;
	InventorySlot item;
	int quantity;
	PUT(int x, int y, InventorySlot item, int quantity):
		Command(CommandType::PUT),
		x(x),
		y(y),
		item(item),
		quantity(quantity) {};
};

struct TAKE: Command {
	int x, y;
	InventorySlot item;
	int quantity;
	TAKE(int x, int y, InventorySlot item, int quantity):
		Command(CommandType::TAKE),
		x(x),
		y(y),
		item(item),
		quantity(quantity) {};
};

struct CRAFT: Command {
	Tool tool;
	CRAFT(Tool tool): Command(CommandType::CRAFT), tool(tool) {};
};

struct MOVE: Command {
	int x, y;
	MOVE(int x, int y): Command(CommandType::MOVE), x(x), y(y) {};
};


void greet_server (const char *name, const char *color);

void send_commands (const std::vector<Command>& cmd);

void end_communication ();


#endif
