#include "common.h"
#include <iostream>
#include <queue>
#include <deque>

using namespace std;

#define NAME "lepsie_cpp"
#define COLOR "de3163"

int DX[] = {0, 1, 0, -1};
int DY[] = {-1, 0, 1, 0};

struct Point {
    int x, y;
};

World world;

bool ma_krompac(const Lemur& l) {
    for (int i = 0; i < l.tools.size(); i++) {
        if (l.tools[i] == Tool::PICKAXE) return true;
    }
    return false;
}


template<class T>
bool is_in(int x, int y, const vector<vector<T>>& v) {
    return x >= 0 && y >= 0 && x < v.size() && y < v[0].size(); //&& world.tiles[x][y].type == TileType::EMPTY;
}

Command pohnem_lemurom(int x, int y, const vector<vector<int>>& bfs_pole) {
    int minimum = 999999999;
    Command cmd = NOOP();
    for (int j=0;j<4;j++){
        int nx = x+DX[j];
        int ny = y+DY[j];
        if (is_in(ny, nx, bfs_pole) && bfs_pole[ny][nx] != -1 && bfs_pole[ny][nx] < minimum) {
            minimum = bfs_pole[ny][nx];
            cmd = MOVE (nx,ny);
        }
    }
    return cmd;
}

Command vezmem_lemon(int x, int y, Command& cmd) {
    for (int j=0;j<4;j++){
        int nx = x+DX[j];
        int ny = y+DY[j];
        if (is_in(ny, nx, world.tiles) && world.tiles[ny][nx].type == TileType::TREE && world.tiles[ny][nx].lemon > 0) {
            cmd = TAKE (nx,ny, InventorySlot::LEMON, world.tiles[ny][nx].lemon);
        }
    }
    return cmd;
}

Command lemon_do_turbiny(int x, int y, Command& cmd, int pocet) {
    for (int j=0;j<4;j++){
        int nx = x+DX[j];
        int ny = y+DY[j];
        if (is_in(ny, nx, world.tiles) && world.tiles[ny][nx].type == TileType::TURBINE && pocet > 0) {
            cmd = PUT (nx,ny, InventorySlot::LEMON, pocet);
        }
    }
    return cmd;
}

Command kopem(Command& cmd, const Lemur& l, TileType a) {
    for (int j=0;j<4;j++){
        int nx = l.x+DX[j];
        int ny = l.y+DY[j];
        if (is_in(ny, nx, world.tiles) && world.tiles[ny][nx].type == a && ma_krompac(l)) {
            cmd = BREAK (nx,ny);
        }
    }
    return cmd;
}

vector<vector<int>> bfs2 (deque<Point>& Q, auto cez_co){
    vector<vector<int>> kamene (world.height, vector<int>(world.width, -1));

    for (int i = 0; i < Q.size(); i++) {
        kamene[Q[i].x][Q[i].y] = 0;
    }

    while (!Q.empty()) {
        Point top = Q.front();
        Q.pop_front();
        for (int i = 0; i < 4; i++) {
            int x = top.x+DX[i];
            int y = top.y+DY[i];
            if (is_in(x, y, kamene) && kamene[x][y] == -1 && cez_co(x,y)){
                Q.push_back({x, y});
                kamene[x][y] = kamene[top.x][top.y]+1;
            }
        }
    }

    return kamene;
}

vector<vector<int>> bfs3 (auto odkial, auto cez_co){
    deque<Point> Q;
    for (int i = 0; i < world.height; i++) {
        for (int j = 0; j < world.width; j++) {
            if (odkial(i,j)) {
                Q.push_back({i,j});
            }
        } 
    }
    return bfs2(Q,cez_co);
}


vector<vector<int>> bfs (TileType a){
    vector<vector<int>> kamene (world.height, vector<int>(world.width, -1));
    queue<Point> Q;

    for (int i = 0; i < world.height; i++) {
        for (int j = 0; j < world.width; j++) {
            if (world.tiles[i][j].type == a) {
                Q.push({i,j});
                kamene[i][j] = 0;
            }
        } 
    }
    while (!Q.empty()) {
        Point top = Q.front();
        Q.pop();
        for (int i = 0; i < 4; i++) {
            if (is_in(top.x+DX[i], top.y+DY[i], kamene) && kamene[top.x+DX[i]][top.y+DY[i]] == -1 && world.tiles[top.x+DX[i]][top.y+DY[i]].type == TileType::EMPTY){
                Q.push({top.x+DX[i], top.y+DY[i]});
                kamene[top.x+DX[i]][top.y+DY[i]] = kamene[top.x][top.y]+1;
            }
        }
    }
    return kamene;
}

bool stromy_s_citronmi (int x, int y) {
    return world.tiles[x][y].type == TileType::TREE && world.tiles[x][y].lemon > 0;
}

bool volne_s_kyslikom (int x, int y) {
    return world.tiles[x][y].type == TileType::EMPTY && world.oxygen[x][y] > 0;
}

bool volne (int x, int y) {
    return world.tiles[x][y].type == TileType::EMPTY;
}

bool je_turbina (int x, int y) {
    return world.tiles[x][y].type == TileType::TURBINE;
}

bool je_kamen (int x, int y) {
    return world.tiles[x][y].type == TileType::STONE;
}

bool je_zelezo (int x, int y) {
    return world.tiles[x][y].type == TileType::IRON;
}



// sem pis svoj kod
vector<Command> do_turn() {
    Player &myself = world.players[world.my_id];
    /*for (int i=0;i<myself.lemurs.size();i++){
        commands [i] = MOVE ()
    }
    if(world.tiles[0][0] == TileType::STONE) {
        
    }*/
    for (int i = 0; i < world.players.size(); i++) {
        if (world.players[i].alive) {
            for (int j = 0; j < world.players[i].lemurs.size(); j++) {
                const Lemur& l = world.players[i].lemurs[j];
                if (l.alive) {
                    world.tiles[l.y][l.x].type = TileType::LEMUR;
                }
            }
        }
    }

    vector<Command> commands(myself.lemurs.size(), NOOP());

    vector<vector<int>> kamene = bfs3(je_kamen, volne_s_kyslikom);

    //vector<vector<int>> stromy = bfs(TileType::TREE);

    vector<vector<int>> zelezo = bfs3(je_zelezo, volne_s_kyslikom);
    //vector<vector<int>> turbina = bfs(TileType::TURBINE);
    vector<vector<int>> turbina = bfs3(je_turbina, volne);
    vector<vector<int>> stromy = bfs3(stromy_s_citronmi, volne_s_kyslikom);


    if (myself.lemurs.size() == 1){
        for (int i=0;i<myself.lemurs.size();i++){
            const auto &lemur = myself.lemurs[i];
            commands[i] = pohnem_lemurom(lemur.x, lemur.y, stromy);
        }
    }


    else {
        for (int i=0;i<myself.lemurs.size();i++){
            const auto &lemur = myself.lemurs[i];
            if (i%4 >= 1){
                commands[i] = pohnem_lemurom(lemur.x, lemur.y, stromy);         
            }
            else if (ma_krompac(lemur) && kamene[lemur.y][lemur.x] < 17) {
                if (i%4 == 0){  //iba tazi kamene
                    commands[i] = pohnem_lemurom(lemur.x, lemur.y, kamene); 
                }
                if (i%4 == 2){  //tazi kamene +ma noz
                    commands[i] = pohnem_lemurom(lemur.x, lemur.y, kamene);
                }   
                if (i%4 == 3 && i!=3){  //tazi iron +ma palicu
                    commands[i] = pohnem_lemurom(lemur.x, lemur.y, zelezo);
                }
            } 
        }
    }


    for (int i=0;i<myself.lemurs.size();i++){
        const auto &lemur = myself.lemurs[i];
        if (lemur.lemon >= 2){
            commands[i] = pohnem_lemurom(lemur.x, lemur.y, turbina);
        }   
    }


    int p = 0, s =0;

    /*for (int i=0;i<myself.lemurs.size();i++){
        const auto &lemur = myself.lemurs[i];
        if (lemur.iron >= 1 && p <= myself.lemurs.size() * 1/4){
            commands[i] = CRAFT (Tool::PICKAXE);
            p++;
            

            
        }

      
        else if (lemur.stone >= 5 && s < 2){
            s++;
            commands[i] = pohnem_lemurom(lemur.x, lemur.y, zelezo);
            for (int j=0;j<4;j++){
                //if (turbina[lemur.y+DY[j]][lemur.x+DX[j]] == 0)
                //    commands [i] = BUILD ( lemur.x, lemur.y, TileType::TREE);
            }

        }
    }*/


  /*     for (int i=0;i<myself.lemurs.size();i++){
        const auto &lemur = myself.lemurs[i];
        if (lemur.stone >= 2 && p <= myself.lemurs.size() * 3/4){
            commands[i] = CRAFT (Tool::PICKAXE);
            p++;
        }

      
        else if (lemur.stone >= 5 && s < 2){
            s++;
            //pod domou
            //commands[i] = BUILD ( , ,TileType::TREE);
        }
    }*/




    /*for (int t=0;t<m;t++)
    for (int i = 0; i < 4; i++) {
        if (kamene[myself.lemurs.x+DX[i]][myself.lemurs.y+DY[i]] > kamene[myself.lemurs.x][myself.lemurs.y]) {  // nico takeho ze ak to vedla teba je mensie ako tz tak tam mas ist (mas ist na to najmensie)
            
        }
    }    */

//   cerr << world.players;
//   cerr << myself;
    cerr << kamene;
    for (int i=0;i<myself.lemurs.size();i++){
        const auto &lemur = myself.lemurs[i];
        commands[i] = kopem(commands[i], lemur, TileType::STONE);
        commands[i] = kopem(commands[i], lemur, TileType::IRON);
        commands[i] = lemon_do_turbiny(lemur.x, lemur.y, commands[i], lemur.lemon);
        commands[i] = vezmem_lemon(lemur.x, lemur.y, commands[i]);
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

