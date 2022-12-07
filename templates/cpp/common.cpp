#include "common.h"

//uplne nezaujimave nemusis citat
//definuje iba format komunikacie so serverom

std::ostream& operator<< (std::ostream& out, const std::vector<Player>& v) {
	std::ranges::copy(v, std::ostream_iterator<Player>(out, " "));
	return out;
}

std::istream& operator>> (std::istream& in, TileType& t) {
	int a;
	in >> a;
	t = static_cast<TileType>(a);
	return in;
}

std::ostream& operator<< (std::ostream& out, const Command& cmd) {
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

std::ostream& operator<< (std::ostream& out, const Tool& t) {
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

std::istream& operator>> (std::istream& in, Tool& t) {
	int a;
	in >> a;
	t = static_cast<Tool>(a);
	return in;
}

std::ostream& operator<< (std::ostream& out, const TileType& t) {
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

void greet_server (const char *name, const char *color) {
	std::string hello;
	char dot;
	std::cin >> hello >> dot;
	std::cout << name << ' ' << color << "\n." << std::endl;
}

void send_commands (const std::vector<Command>& commands) {
	std::ranges::copy(commands, std::ostream_iterator<Command>(std::cout, "\n"));
	std::cout << '.' << std::endl;
}

int Player::_id = 0;
