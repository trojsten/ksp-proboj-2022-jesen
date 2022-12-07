#include "common.h"

using namespace std;

#define NAME "cpp"
#define COLOR "00ff00"

int DX[] = {0, 1, 0, -1};
int DY[] = {-1, 0, 1, 0};

World world;

// sem pis svoj kod
vector<Command> do_turn() {
    Player &myself = world.players[world.my_id];
    vector<Command> commands(myself.lemurs.size(), NOOP());
    cerr << world.players;
    cerr << myself;

    return commands;
}

int main() {
    // aby sme mali nahodu
    srand(time(nullptr));
    // povieme serveru ako sa chceme volat a farbu
    greet_server(NAME, COLOR);
    // robime tahy kym sme zivy
    do {
        cin >> world;
        send_commands(do_turn());
    } while (world.players[world.my_id].alive);
    cout << "Bye\n";
}

