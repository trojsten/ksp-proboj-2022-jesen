#include "common.h"

using namespace std;

#define NAME "cpp"
#define COLOR "00ff00"

int DX[] = {0, 1, 0, -1};
int DY[] = {-1, 0, 1, 0};

World world;

// sem pis svoj kod
vector<Command> do_turn() {
    Player& myself = world.players[world.my_id];
	int pocet_lemurov = myself.lemurs.size();
	vector<Command> commands(pocet_lemurov, NOOP());



	/*for (int i = 0; i < pocet_lemurov; i++) {
		Lemur& l = myself.lemurs[i];
        cerr << l << endl;
        cerr << "l-"<<i<<" "<<world.oxygen[l.x][l.y]<<endl;
		if (l.alive) {
			int random = rand() % 4;
			// ak je zivy, tak sa pohne nahodne
			commands[i] = MOVE(l.x + DX[random], l.y + DY[random]);
			//cerr << commands[i] << endl;
		}
	}*/
    for(int i=0;i<pocet_lemurov;i++){
        Lemur& l = myself.lemurs[i];
        for(int j=0; j<=3;j++){
            if(world.oxygen[l.x+DX[j]][l.y+DY[j]]>world.oxygen[l.x][l.y]){
                commands[i] = MOVE(l.x + DX[j], l.y + DY[j]);
            }
        }
        cerr << l << endl;
        cerr << "l-"<<i<<" "<<world.oxygen[l.x][l.y]<<endl;
    }
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

