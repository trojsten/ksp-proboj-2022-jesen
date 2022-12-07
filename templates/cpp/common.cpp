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

std::ostream& operator<< (std::ostream& out, const CommandType& cmd) {
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

std::ostream& operator<< (std::ostream& out, const InventorySlot& i) {
	out << static_cast<int>(i);
	return out;
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

std::ostream& operator<< (std::ostream& out, const Command& cmd) {
	out << cmd.type;
	switch (cmd.type) {
		case CommandType::NOOP:
			break;
		case CommandType::STAB:
			out << " " << static_cast<const STAB&>(cmd).x;
			out << " " << static_cast<const STAB&>(cmd).y;
			break;
		case CommandType::BONK:
			out << " " << static_cast<const BONK&>(cmd).x;
			out << " " << static_cast<const BONK&>(cmd).y;
			break;
		case CommandType::BUILD:
			out << " " << static_cast<const BUILD&>(cmd).x;
			out << " " << static_cast<const BUILD&>(cmd).y;
			out << " " << static_cast<const BUILD&>(cmd).tile;
			break;
		case CommandType::BREAK:
			out << " " << static_cast<const BREAK&>(cmd).x;
			out << " " << static_cast<const BREAK&>(cmd).y;
			break;
		case CommandType::DISCARD:
			out << " " << static_cast<const DISCARD&>(cmd).item;
			out << " " << static_cast<const DISCARD&>(cmd).quantity;
			break;
		case CommandType::PUT:
			out << " " << static_cast<const PUT&>(cmd).x;
			out << " " << static_cast<const PUT&>(cmd).y;
			out << " " << static_cast<const PUT&>(cmd).item;
			out << " " << static_cast<const PUT&>(cmd).quantity;
			break;
		case CommandType::TAKE:
			out << " " << static_cast<const TAKE&>(cmd).x;
			out << " " << static_cast<const TAKE&>(cmd).y;
			out << " " << static_cast<const TAKE&>(cmd).item;
			out << " " << static_cast<const TAKE&>(cmd).quantity;
			break;
		case CommandType::CRAFT:
			out << " " << static_cast<int>(static_cast<const CRAFT&>(cmd).tool);
			break;
		case CommandType::MOVE:
			out << " " << static_cast<const MOVE&>(cmd).x;
			out << " " << static_cast<const MOVE&>(cmd).y;
			break;
	}
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
