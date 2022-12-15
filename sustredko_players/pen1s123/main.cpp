#include "common.h"
#include<queue>

using namespace std;

#define NAME "DivoStena"
#define COLOR "aa4a44"
#define fst first
#define snd second

const int INT_MAX = 1<<30;

struct Objekt{
    int x,y;
    TileType typ;
    Objekt(int a = INT_MAX,int b = INT_MAX,TileType t = TileType::EMPTY){
        x = a;
        y = b;
        typ = t;
    }
};

//#############################################################
//Global Variables


int DX[] = {1, 0, -1};
int DY[] = {0, 1, -1};
pair<int,int> SMERY[] = {{0,1},{0,-1},{1,0},{-1,0}};
vector<int> roles; //kto co robi, 1 - Udrziavaj 2 - Mine
vector<Objekt> lemurStrom; //[indexLemura] => priradeny strom
vector<Objekt> turbiny; //zoznam turbin, ku ktorym sa vieme dostat
Objekt nasaTurbina; //nasa domovska turbina
int nasaTurbinaIndex; //index nasej domovskej turbiny
vector<Objekt> stromy; //zoznam stromov, ku ktorym sa vieme dostat
vector<vector<pair<Objekt, bool>>> StromyTurbiny; //[indexTurbiny][indexPriradenehoStromu] =>{strom,zabraty}
vector<vector<int>> safeDist; //[y][x] =>vzdialeonst k najblizsej turbine
bool maloStromov = 0;
vector<int> citronyTahy; // kolko mame citronov v tahu i
int currTah = 0;
float derivaciaCitronov = -1;  //magicka konstanta je 0.1
float MagickaKonstanta = 0.1;
bool chcemCitrony = 0;
bool stavam = 0;
vector<Objekt> vsetkyTurbiny;
Objekt utocnyKeket;
Objekt obstavanieSpot;

World world;

//utility
int dist(int x1, int y1, int x2, int y2) { return abs(x1 - x2) + abs(y1 - y2); }
int dist(pair<int,int> p1, pair<int,int> p2){ return abs(p1.first - p2.first) + abs(p1.second - p2.second); }
int dist(Objekt p1, Objekt p2){ return abs(p1.x - p2.x) + abs(p1.y - p2.y); }
int dist(Objekt p1, Lemur l2){ return abs(p1.x - l2.x) + abs(p1.y - l2.y); }
bool MamTool(Lemur ja,Tool co){
    return ja.tools[0] == co || ja.tools[1] == co;
}
bool MamJuicer(Lemur ja){
    return ja.tools[0] == Tool::JUICER || ja.tools[1] == Tool::JUICER;
}
bool Volne(int x,int y){
    return x >= 0 && y >= 0 && x < world.width && y < world.height && (world.tiles[y][x].type == TileType::EMPTY || world.tiles[y][x].type == TileType::ALLY);
}
bool MamVolne(Lemur ja){
    return ja.tools[0] == Tool::NO_TOOL || ja.tools[1] == Tool::NO_TOOL;
}
bool Vnutry(int x,int y){
    return x >= 0 && y >= 0 && x < world.width && y < world.height;
}
bool SomSafe(Lemur ja){
    if(!Vnutry(ja.x,ja.y)) return 0;
    int dist = safeDist[ja.y][ja.x];
    return dist <= 14 || (MamJuicer(ja) && ja.lemon/5 >= dist - 14);
}
bool SomSafe(int x,int y, bool mamJuicer,int lemon){
    if(!Vnutry(x,y)) return 0;
    int dist = safeDist[y][x];
    //cerr<<"vzdialenost od vrtule "<<dist<<" pre sur "<<x<<" "<<y<<endl;
    return dist <= 14 || (mamJuicer && lemon/5 >= dist - 14);
}


//#############################################################
//Innit funkcie

void GetDosiahnutelne(){
    Player &myself = world.players[world.my_id];
    queue<pair<int,int>> q;
    q.push({myself.lemurs[0].x,myself.lemurs[0].y});
    vector<vector<int>> vzd(world.height,vector<int>(world.width,-1));
    vzd[myself.lemurs[0].y][myself.lemurs[0].x] = 0;
    while(!q.empty()){
        pair<int,int> cur = q.front();q.pop();
        for(auto i : SMERY){
            if(Volne(cur.fst + i.fst,cur.snd + i.snd) && vzd[cur.snd + i.snd][cur.fst + i.fst] == -1){
                q.push({cur.fst + i.fst,cur.snd + i.snd});
                vzd[cur.snd + i.snd][cur.fst + i.fst] = vzd[cur.snd][cur.fst]+1;
            }
            if(Vnutry(cur.fst + i.fst,cur.snd + i.snd) && world.tiles[cur.snd + i.snd][cur.fst + i.fst].type == TileType::TREE && vzd[cur.snd + i.snd][cur.fst + i.fst] == -1){
                //cerr << "nasiel som objekt na " << cur.fst + i.fst << " " << cur.snd + i.snd << endl;
                stromy.push_back(Objekt(cur.fst + i.fst, cur.snd + i.snd, TileType::TREE));
                vzd[cur.snd + i.snd][cur.fst + i.fst] = vzd[cur.snd][cur.fst]+1;
            }
            if(Vnutry(cur.fst + i.fst,cur.snd + i.snd) && world.tiles[cur.snd + i.snd][cur.fst + i.fst].type == TileType::TURBINE && vzd[cur.snd + i.snd][cur.fst + i.fst] == -1){
                //cerr << "nasiel som objekt na " << cur.fst + i.fst << " " << cur.snd + i.snd << endl;
                turbiny.push_back(Objekt(cur.fst + i.fst, cur.snd + i.snd, TileType::TURBINE));
                vzd[cur.snd + i.snd][cur.fst + i.fst] = vzd[cur.snd][cur.fst]+1;
            }
        }
    }
    cerr << "nase turbiny: " << endl;
    for(auto i : turbiny)cerr << i.x << " " << i.y<<";"; cerr << endl;
    cerr << "nase lemurStrom: " << endl;
    for(auto i : stromy)cerr << i.x << " " << i.y<<";";cerr << endl;
    int j = 0;
    for(auto i : turbiny){
        if(dist(i, myself.lemurs[0]) < dist(nasaTurbina, myself.lemurs[0])){
            nasaTurbina = i;
            nasaTurbinaIndex = j;
        }
        j++;
    }
}

void GetCitronyGeneratory(){
    StromyTurbiny.resize(turbiny.size(),vector<pair<Objekt,bool>>());
    for(auto s : stromy){
        Objekt nT;
        int ni = 0;
        int i = 0;
        for(auto t : turbiny){
            if(dist(s,t) < dist(s,nT)){
                nT = t;
                ni = i;
            }
            i++;
        }
        if(dist(nT, s) <= 15){
            StromyTurbiny[ni].push_back({s, false});
        }
        else{
        }
    }
}

void findTurbines(){
    for(int i = 0;i<world.height;i++)for(int j = 0;j<world.width;j++){
        if(world.tiles[i][j].type == TileType::TURBINE && (i != nasaTurbina.y || j != nasaTurbina.x)) vsetkyTurbiny.push_back(Objekt(j,i,TileType::TURBINE));
    }
}


//################################################################
//Utility funkcie

int real_dist(Objekt start, Objekt finish){
    queue<pair<int,int>> q;
    q.push({start.x,finish.y});
    vector<vector<int>> vzd(world.height,vector<int>(world.width,-1));
    vzd[start.y][start.x] = 0;
    while(!q.empty()){
        pair<int,int> cur = q.front();q.pop();
        for(auto i : SMERY){
            if(Volne(cur.fst + i.fst,cur.snd + i.snd) && vzd[cur.snd + i.snd][cur.fst + i.fst] == -1){
                q.push({cur.fst + i.fst,cur.snd + i.snd});
                vzd[cur.snd + i.snd][cur.fst + i.fst] = vzd[cur.snd][cur.fst]+1;
            }
            if(Vnutry(cur.fst + i.fst,cur.snd + i.snd) && cur.fst + i.fst == finish.x && cur.fst + i.fst == finish.y){ 
                //cerr << "nasiel som objekt na " << cur.fst + i.fst << " " << cur.snd + i.snd << endl;
                return vzd[cur.snd][cur.fst] + 1;
            }
        }
    }
    return INT_MAX;
}

void calculateSafeDist(){
    queue<pair<int,int>> q;
    safeDist.assign(world.height,vector<int>(world.width,-1));
    for(auto i : turbiny){
        q.push({i.x,i.y});
        safeDist[i.y][i.x] = 0;
    }
    while(!q.empty()){
        pair<int,int> cur = q.front();q.pop();
        for(auto i : SMERY){
            if(Volne(cur.fst + i.fst,cur.snd + i.snd) && safeDist[cur.snd + i.snd][cur.fst + i.fst] == -1){
                q.push({cur.fst + i.fst,cur.snd + i.snd});
                safeDist[cur.snd + i.snd][cur.fst + i.fst] = safeDist[cur.snd][cur.fst]+1;
            }
        }
    }
}

int numOfFree(int x,int y){
    int ret = 0;
    for(int i = 0;i<3;i++)for(int j = 0;j<3;j++){
        int dx = DX[i],dy = DY[j];
        if (Vnutry(x + dx, y + dy) && (world.tiles[y+dy][x+dx].type == TileType::EMPTY || world.tiles[y+dy][x+dx].type == TileType::OBSADENE || world.tiles[y+dy][x+dx].type == TileType::ALLY)) ret ++; 
    }
    return ret;
}

Objekt Nearest(TileType type, Objekt ja,bool inSafeZone = 0){
    queue<pair<int,int>> q;
    q.push({ja.x,ja.y});
    vector<vector<int>> vzd(world.height,vector<int>(world.width,-1));
    vzd[ja.y][ja.x] = 0;
    while(!q.empty()){
        pair<int,int> cur = q.front();q.pop();
        for(auto i : SMERY){
            if(Volne(cur.fst + i.fst,cur.snd + i.snd) && vzd[cur.snd + i.snd][cur.fst + i.fst] == -1 && !(inSafeZone && safeDist[cur.snd + i.snd][cur.fst + i.fst] > 14)){
                q.push({cur.fst + i.fst,cur.snd + i.snd});
                vzd[cur.snd + i.snd][cur.fst + i.fst] = vzd[cur.snd][cur.fst]+1;
            }
            if(Vnutry(cur.fst + i.fst,cur.snd + i.snd) && world.tiles[cur.snd + i.snd][cur.fst + i.fst].type == type){
                //cerr << "nasiel som objekt na " << cur.fst + i.fst << " " << cur.snd + i.snd << endl;
                return Objekt(cur.fst + i.fst, cur.snd + i.snd, type);
            }
        }
    }
    return Objekt(-1,-1,TileType::EMPTY);
}

void editMap(){
    for(int i = 0;i < world.players.size();i++)
        if(i != world.my_id && world.players[i].alive){
        for(Lemur j : world.players[i].lemurs)if(j.alive){
            world.tiles[j.y][j.x].type = TileType::ENEMY;
        } 
    }
    for(Lemur j : world.players[world.my_id].lemurs)if(j.alive){
        world.tiles[j.y][j.x].type = TileType::ALLY;
    }
}

Objekt najdiStrom(Lemur currLemur){ 
    Objekt strom = Objekt();
    if(StromyTurbiny[nasaTurbinaIndex].size() == 0){
        maloStromov = true;
        return Objekt();
    }
    int j = 0;
    int minj = 0;
    for(auto s : StromyTurbiny[nasaTurbinaIndex]){
        if(!s.second){
            if(dist(s.first, currLemur) < dist(strom, currLemur)){
                strom = s.first;
                minj = j;
            }
        }
        j++;
    }
    if(strom.x == INT_MAX){
        maloStromov = true;
    }
    else{
        StromyTurbiny[nasaTurbinaIndex][minj].second = true;
    }
    return strom;
}

Objekt bestSpotForTree(int limit = 9){
    queue<pair<int,int>> q;
    q.push({nasaTurbina.x, nasaTurbina.y});
    vector<vector<int>> vzd(world.height,vector<int>(world.width,-1));
    vzd[nasaTurbina.y][nasaTurbina.x] = 0;
    while(!q.empty()){
        pair<int,int> cur = q.front();q.pop();
        if(vzd[cur.snd][cur.fst] >= 7) continue;
        for(auto i : SMERY){
            if(Volne(cur.fst + i.fst,cur.snd + i.snd) && vzd[cur.snd + i.snd][cur.fst + i.fst] == -1){
                q.push({cur.fst + i.fst,cur.snd + i.snd});
                vzd[cur.snd + i.snd][cur.fst + i.fst] = vzd[cur.snd][cur.fst]+1;
            }
            if(Vnutry(cur.fst + i.fst,cur.snd + i.snd) && numOfFree(cur.fst + i.fst,cur.snd + i.snd) == limit){
                return Objekt(cur.fst + i.fst, cur.snd + i.snd);
            }
        }
    }
    return Objekt(-1,-1,TileType::EMPTY);
}

pair<int,int> FindPath(Objekt start, Objekt finish,bool juicer = 0,int lemon = 0){
    queue<pair<int,int>> q; //cur x,y
    vector<vector<int>> vzd(world.height,vector<int>(world.width,-1)); //vzd[y][x]
    vector<vector<pair<int,int>>> parent(world.height,vector<pair<int,int>>(world.width)); //parent[y][x] = {x, y}
    vzd[start.y][start.x] = 0;
    parent[start.y][start.x] = {start.x,start.y};
    q.push({start.x,start.y});
    bool nasiel_som = 0;
    while(!q.empty() && !nasiel_som){
        pair<int,int> cur = q.front();q.pop();
        //cerr<<cur.fst<<" "<<cur.snd<<endl;
        for(auto i : SMERY){
            pair<int,int> nv = {cur.fst + i.fst,cur.snd + i.snd};
            if(Volne(nv.fst,nv.snd) && vzd[nv.snd][nv.fst] == -1 && SomSafe(nv.fst,nv.snd,juicer,lemon)){
                q.push({nv.fst,nv.snd});
                vzd[nv.snd][nv.fst] = vzd[cur.snd][cur.fst]+1;
                parent[nv.snd][nv.fst] = {cur.fst,cur.snd};
            }
            if(Vnutry(nv.fst,nv.snd) && nv.fst == finish.x && nv.snd == finish.y){
                nasiel_som = 1;
                vzd[nv.snd][nv.fst] = vzd[cur.snd][cur.fst]+1;
                parent[nv.snd][nv.fst] = {cur.fst,cur.snd};
                break;
            }
        }
    }
    if(nasiel_som){
        vector<pair<int,int>> path(vzd[finish.y][finish.x]);
        pair<int,int> cur{finish.x,finish.y};
        int ind = path.size()-1;
        while(cur != parent[cur.snd][cur.fst]){
            path[ind] = {cur.fst,cur.snd};
            cur = parent[cur.snd][cur.fst];
            ind--;
        }
        //for(auto i : path)cerr<<i.fst<<" "<<i.snd<<";";cerr<<endl;
        //return MOVE(path[0].fst,path[0].snd);
        return {path[0].fst,path[0].snd};
    }else{
        cerr<<"YEETYS"<<endl;
        return {-1,-1};
    }
}

void GetDerivacia(){
    cerr<<currTah <<endl;
    if(currTah >= 8){
        derivaciaCitronov = (float)(citronyTahy[currTah] - citronyTahy[currTah-8])/8;
    }
}

//ovladacie funkcie

Command Udrziavaj(Lemur kto, Objekt co, Objekt kam){
    Objekt ja(kto.x,kto.y,TileType::EMPTY);
    if(chcemCitrony){
        co = utocnyKeket;
    }
    if(kto.lemon){
        pair<int,int> next = FindPath(ja,co, MamJuicer(kto), kto.lemon);
        if(next.fst == co.x && next.snd == co.y){
            return PUT(co.x,co.y,InventorySlot::LEMON,kto.lemon);
        }
        //mozno som to rozbil
        //world.tiles[next.snd][next.fst].type = TileType::OBSADENE;
        return MOVE(next.fst,next.snd);
    }else{
        pair<int,int> next = FindPath(ja,kam, MamJuicer(kto), kto.lemon);
        if(next.fst == kam.x && next.snd == kam.y){
            return TAKE(kam.x,kam.y,InventorySlot::LEMON,1);
        }
        //mozno som to rozbil
        //world.tiles[next.snd][next.fst].type = TileType::OBSADENE;
        return MOVE(next.fst,next.snd);
    }
}

Command Zautoc(Lemur kto, Objekt target){
    Objekt ja(kto.x,kto.y);
    Command move = NOOP();
    pair<int,int> kam = FindPath(ja,target,MamJuicer(kto),kto.lemon);
    if(kam.fst == target.x && kam.snd == target.y){
            move = STAB(kam.fst,kam.snd);
    }else{
        move = MOVE(kam.fst,kam.snd);
    }
    return move;
}

Command ZoberCitrony(Lemur kto){
    Objekt ja(kto.x,kto.y);
    Objekt co = nasaTurbina;
    Tile turbina = world.tiles[co.y][co.x];
    pair<int,int> next = FindPath(ja,co, MamJuicer(kto), kto.lemon);
    if(next.fst == co.x && next.snd == co.y){
        chcemCitrony = 1;
        world.tiles[kto.y][kto.x].type = TileType::STONE;
        if(world.tiles[co.y][co.x].lemon > 5) return NOOP();
        else return PUT(co.x,co.y,InventorySlot::LEMON,1);
        //return TAKE(co.x,co.y,InventorySlot::LEMON,max(0,turbina.lemon));
    }
    //mozno som to rozbil
    //world.tiles[next.snd][next.fst].type = TileType::OBSADENE;
    return MOVE(next.fst,next.snd);
}

Command Utocnik(Lemur kto,int id){
    Objekt ja(kto.x,kto.y);
    Objekt target = Nearest(TileType::ENEMY,ja,1);
    if(derivaciaCitronov < MagickaKonstanta || target.x == -1){
        if(derivaciaCitronov > MagickaKonstanta && MamJuicer(kto)){
            Objekt target_mimo = Nearest(TileType::ENEMY,ja);
            int dist = real_dist(ja,target_mimo);
            if(dist <= kto.lemon/5) return Zautoc(kto,target_mimo);
            else return ZoberCitrony(kto);
        }
        return Udrziavaj(kto,nasaTurbina,lemurStrom[id]);
    }
    return Zautoc(kto,target);
}

Command Idluj(Lemur kto){
    Objekt ja(kto.x,kto.y);
    int r = rand()%4;
    int x = kto.x + SMERY[r].first, y = kto.y + SMERY[r].second;
    if(!Vnutry(x,y)) return NOOP();
    if(SomSafe(x,y,MamJuicer(kto),kto.lemon)) return MOVE(x,y);
    else{
        Objekt turbina = Nearest(TileType::TURBINE,ja);
        pair<int,int> safe = FindPath(ja,turbina,MamJuicer(kto),kto.lemon);
        return MOVE(safe.fst,safe.snd);
    }
}
Command MoveWithMine(Objekt start,Objekt finish){
    queue<pair<int,int>> q; //cur x,y
    vector<vector<int>> vzd(world.height,vector<int>(world.width,-1)); //vzd[y][x]
    vector<vector<pair<int,int>>> parent(world.height,vector<pair<int,int>>(world.width)); //parent[y][x] = {x, y}
    vzd[start.y][start.x] = 0;
    parent[start.y][start.x] = {start.x,start.y};
    q.push({start.x,start.y});
    bool nasiel_som = 0;
    while(!q.empty() && !nasiel_som){
        pair<int,int> cur = q.front();q.pop();
        //cerr<<cur.fst<<" "<<cur.snd<<endl;
        for(auto i : SMERY){
            
            pair<int,int> nv = {cur.fst + i.fst,cur.snd + i.snd};
            if(nv.first == nasaTurbina.x && nv.second == nasaTurbina.y) continue;
            if(Vnutry(nv.fst,nv.snd) && vzd[nv.snd][nv.fst] == -1){
                q.push({nv.fst,nv.snd});
                vzd[nv.snd][nv.fst] = vzd[cur.snd][cur.fst]+1;
                parent[nv.snd][nv.fst] = {cur.fst,cur.snd};
                if(nv.fst == finish.x && nv.snd == finish.y){
                    nasiel_som = 1;
                    break;
                }
            }
        }
    }
    if(nasiel_som){
        vector<pair<int,int>> path(vzd[finish.y][finish.x]);
        pair<int,int> cur{finish.x,finish.y};
        int ind = path.size()-1;
        while(cur != parent[cur.snd][cur.fst]){
            path[ind] = {cur.fst,cur.snd};
            cur = parent[cur.snd][cur.fst];
            ind--;
        }
        //for(auto i : path)cerr<<i.fst<<" "<<i.snd<<";";cerr<<endl;
        //return MOVE(path[0].fst,path[0].snd);
        if(Volne(path[0].fst,path[0].snd)) return MOVE(path[0].fst,path[0].snd);
        else return BREAK(path[0].fst,path[0].snd);
    } 
}

Command ObstavajSa(Lemur kto){
    Objekt ja(kto.x,kto.y);
    
    if(!stavam) obstavanieSpot = bestSpotForTree(9);
    if(obstavanieSpot.x == -1){
        cerr << "neansiel som de stavat :|" << endl;
    }
    if(obstavanieSpot.x == kto.x && obstavanieSpot.y == kto.y){ //mozem stavat
    cerr << "ObstavajSa ##########################################" << endl;
    stavam = 1;
        if(world.tiles[kto.y][kto.x+1].type != TileType::TREE){
            return BUILD(kto.x+1, kto.y, TileType::TREE);
        }
        else if(world.tiles[kto.y+1][kto.x].type != TileType::TREE){
            return BUILD(kto.x, kto.y+1, TileType::TREE);
        }
        else if(world.tiles[kto.y-1][kto.x].type != TileType::TREE){
            return BUILD(kto.x, kto.y-1, TileType::TREE);
        }
        else{
            if(world.tiles[kto.y][kto.x+1].lemon != 0){
                return TAKE(kto.x+1, kto.y, InventorySlot::LEMON, 1);
            }
            else if(world.tiles[kto.y+1][kto.x].lemon != 0){
                return TAKE(kto.x, kto.y+1, InventorySlot::LEMON, 1);
            }
            else if(world.tiles[kto.y-1][kto.x].lemon != 0){
                return TAKE(kto.x, kto.y-1, InventorySlot::LEMON, 1);
            }
        }
    }else{
        pair<int,int> next = FindPath(ja,obstavanieSpot);
        return MOVE(next.first,next.second);
    }
    
    return NOOP();
}


Command UtocnyMiner(Lemur kto){
    cerr<<"mam citrony "<<kto.lemon<<endl;
    Objekt ja(kto.x,kto.y,TileType::EMPTY);
    if(maloStromov){
        if(kto.stone >= 5){
            Objekt miesto;
            for(int l = 9;l>6;l--){
                miesto = bestSpotForTree();
                if(miesto.x != -1) break;
            }
            cerr<<"staviam strom xddd na "<<miesto.x<<" "<<miesto.y<<endl;
            if(miesto.x != -1){
                pair<int,int> smer = FindPath(ja,miesto,MamJuicer(kto),kto.lemon);
                if(smer.fst == miesto.x && smer.snd == miesto.y){
                    StromyTurbiny[nasaTurbinaIndex].push_back({Objekt(miesto.x,miesto.y,TileType::TREE),0});
                    cerr<<"NOVY STROM "<<miesto.x<<" "<<miesto.y<<"--------------------------"<<endl;
                    maloStromov = 0;
                    return BUILD(miesto.x,miesto.y,TileType::TREE);
                }
                cerr<<"idem k miestu na strom-------------"<<endl;
                return MOVE(smer.fst,smer.snd);
            }
        }
        else{ //tazim kamene
            Objekt suter = Nearest(TileType::STONE,ja,!MamJuicer(kto));
            if(suter.x != -1){
                pair<int,int> kam = FindPath(ja,suter,MamJuicer(kto),kto.lemon);
                if(kam.fst == suter.x && kam.snd == suter.y){
                    cerr<<"tazim suter------------------------"<<endl;
                    return BREAK(kam.fst,kam.snd);
                }
                    cerr<<"idem za sutrom "<<suter.x<<" "<<suter.y<<endl;
                    if(kam.fst == -1) return Idluj(kto);
                    return MOVE(kam.fst,kam.snd);
            }
        }
    }
    else{ //netreba stromy ideme utocit
        Objekt target_with_juicer = Nearest(TileType::ENEMY,ja,!MamJuicer(kto));
        Objekt target = Nearest(TileType::ENEMY,ja,1);
        cerr<<"POSSIBLE TARGETS"<<target.x<<" "<<target.y<<";"<<target_with_juicer.x<<" "<<target_with_juicer.y<<endl;
        if(kto.iron == 0){
            Objekt iron = Nearest(TileType::IRON,ja,!MamJuicer(kto));
            if(!maloStromov && iron.x != -1){
                pair<int,int> kam = FindPath(ja,iron,MamJuicer(kto),kto.lemon);
                if(kam.fst == iron.x && kam.snd == iron.y){
                    cerr<<"tazim zelezo-------------------------"<<endl;
                    return BREAK(kam.fst,kam.snd);
                }
                cerr<<"idem za zelezom "<<iron.x<<" "<<iron.y<<endl;
                if(kam.fst == -1) return Idluj(kto);
                return MOVE(kam.fst,kam.snd);
                
            }
        }
        if(target.x != -1){ //targen in range
            if(MamTool(kto,Tool::KNIFE)){
                return Zautoc(kto,target);
            }
            if(MamVolne(kto)) return CRAFT(Tool::KNIFE);
            return DISCARD(InventorySlot::TOOL1,1);
        }
        int dist_to_base = INT_MAX;
        Objekt bestBase;
        for(auto i : vsetkyTurbiny){
            cerr << "turbina " << i.x << " " << i.y << endl;
            if(world.tiles[i.y][i.x].lemon && dist_to_base > dist(i,ja)){
                dist_to_base = dist(i,ja);
                bestBase = i;
            }
        }
        cerr << "bestBase" << bestBase.x << " " << bestBase.y << endl;
        if(bestBase.x != INT_MAX){
            int time = 2*dist_to_base;
            if(kto.lemon*5 >= time){
                return MoveWithMine(ja,bestBase);
            }
        }
        if(kto.stone < 18 && !stavam){ //nemam sutre na juicer
            Objekt suter = Nearest(TileType::STONE,ja,!MamJuicer(kto));
            if(suter.x != -1){
                pair<int,int> kam = FindPath(ja,suter,MamJuicer(kto),kto.lemon);
                if(kam.fst == suter.x && kam.snd == suter.y){
                    cerr<<"tazim suter------------------------"<<endl;
                    return BREAK(kam.fst,kam.snd);
                }
                cerr<<"idem za sutrom "<<suter.x<<" "<<suter.y<<endl;
                if(kam.fst == -1) return Idluj(kto);
                return MOVE(kam.fst,kam.snd);
            }
        }
        if(!MamTool(kto,Tool::JUICER) && kto.stone >= 3) return CRAFT(Tool::JUICER);
        return ObstavajSa(kto);
    }
    return Idluj(kto);
}

Command Mine(Lemur kto){
    Objekt ja(kto.x,kto.y,TileType::EMPTY);
    Command move = Idluj(kto);
    bool set = 0;
    //mam dost resources na postavenie stromu
    Objekt target_with_juicer = Nearest(TileType::ENEMY,ja,!MamJuicer(kto));
    Objekt target = Nearest(TileType::ENEMY,ja,1);
    if(maloStromov && kto.stone >= 5){
        Objekt miesto;
        for(int l = 9;l>6;l--){
            miesto = bestSpotForTree();
            if(miesto.x != -1) break;
        }
        cerr<<"staviam strom xddd na "<<miesto.x<<" "<<miesto.y<<endl;
        if(miesto.x != -1){
            pair<int,int> smer = FindPath(ja,miesto,MamJuicer(kto),kto.lemon);
            if(smer.fst == miesto.x && smer.snd == miesto.y){
                set = 1;
                move = BUILD(miesto.x,miesto.y,TileType::TREE);
                StromyTurbiny[nasaTurbinaIndex].push_back({Objekt(miesto.x,miesto.y,TileType::TREE),0});
                cerr<<"NOVY STROM "<<miesto.x<<" "<<miesto.y<<"--------------------------"<<endl;
                maloStromov = 0;
            }
            else{
                set = 1;
                cerr<<"idem k miestu na strom-------------"<<endl;
                move = MOVE(smer.fst,smer.snd);
            }
        }
    }else if(kto.iron && MamVolne(kto)){
        set = 1;
        cerr<<"Craftim iteeem-----------------------"<<endl;
        return CRAFT(Tool::KNIFE);
    }else if(MamTool(kto,Tool::KNIFE) && target.x != -1){
        set = 1;
        cerr<<"Idem utocit-----------------------"<<endl;
        move = Zautoc(kto,target);
    }else if(MamTool(kto,Tool::KNIFE) && target_with_juicer.x != -1){
        set = 1;
        cerr<<"Idem utocit-----------------------"<<endl;
        move = Zautoc(kto,target_with_juicer);
    }
    /*else if(derivaciaCitronov > MagickaKonstanta && kto.iron >= 1){//viem dakomu dat pickaxe/noz/juicer a chcem to
        Objekt target = Nearest(TileType::ALLY,ja,!MamJuicer(kto));
        pair<int,int> kam = FindPath(ja,target,MamJuicer(kto),kto.lemon);
        if(kam.fst == target.x && kam.snd == target.y){
                move = PUT(kam.fst,kam.snd, InventorySlot::IRON, 1);
        }else{
            move = MOVE(kam.fst,kam.snd);
        }
    }else if(derivaciaCitronov > MagickaKonstanta && kto.stone >= 3){
        cerr<<"chcem dat kamen---------------------------------------------------"<<endl;
        Objekt target = Nearest(TileType::ALLY,ja,!MamJuicer(kto));
        pair<int,int> kam = FindPath(ja,target,MamJuicer(kto),kto.lemon);
        if(kam.fst == target.x && kam.snd == target.y){
                move = PUT(kam.fst,kam.snd, InventorySlot::STONE, 3);
                cerr<<"DODOVZDAL SOM SUROVINY--------------------------------------"<<endl;
        }else{
            move = MOVE(kam.fst,kam.snd);
        }
        }*/
    if(!set) { //default
        Objekt suter = Nearest(TileType::STONE,ja,!MamJuicer(kto));
        Objekt iron = Nearest(TileType::IRON,ja,!MamJuicer(kto));
        if(!maloStromov && iron.x != -1){
            pair<int,int> kam = FindPath(ja,iron,MamJuicer(kto),kto.lemon);
            if(kam.fst == iron.x && kam.snd == iron.y){
                cerr<<"tazim zelezo-------------------------"<<endl;
                move = BREAK(kam.fst,kam.snd);
            }else{
                cerr<<"idem za zelezom "<<iron.x<<" "<<iron.y<<endl;
                move = MOVE(kam.fst,kam.snd);
            }
        }else if(suter.x != -1){
            pair<int,int> kam = FindPath(ja,suter,MamJuicer(kto),kto.lemon);
            if(kam.fst == suter.x && kam.snd == suter.y){
                cerr<<"tazim suter------------------------"<<endl;
                move = BREAK(kam.fst,kam.snd);
            }else{
                cerr<<"idem za sutrom "<<suter.x<<" "<<suter.y<<endl;
                move = MOVE(kam.fst,kam.snd);
            }
        }
    }
    if(SomSafe(kto)){
        //world.tiles[move.y][move.x].type = TileType::OBSADENE;
        return move;
    }
    else{
        Objekt turbina = Nearest(TileType::TURBINE,ja);
        pair<int,int> safe = FindPath(ja,turbina,MamJuicer(kto),kto.lemon);
        return MOVE(safe.fst,safe.snd);
    }
}

//#############################################################
// Do Turn
vector<Command> do_turn() {
    calculateSafeDist();
    editMap();
    cerr << "citrony :" << world.tiles[nasaTurbina.y][nasaTurbina.x].lemon << endl;
    citronyTahy.push_back(world.tiles[nasaTurbina.y][nasaTurbina.x].lemon);
    GetDerivacia();
    cerr << "Derivacia tento tah " << derivaciaCitronov << endl;
    Player &myself = world.players[world.my_id];
    //cerr<<"Nasi yeetusy: ";for(auto i : myself.lemurs)cerr<<i.x<<" "<<i.y<<";";cerr<<endl;
    vector<Command> commands(myself.lemurs.size(), NOOP());
    
    Lemur currlemur;
    for(int i = 0; i < myself.lemurs.size(); i++) {
        currlemur = myself.lemurs[i];
        Objekt ja(currlemur.x,myself.lemurs[i].y);
        if(currlemur.stone && roles[i] != 2){
            commands[i] = CRAFT(Tool::JUICER);
            cerr << "Dostal som Juicer" << endl;
            continue;
        }
        if(currlemur.iron && roles[i] != 2){
            commands[i] = CRAFT(Tool::KNIFE);
            roles[i] = 3;
            cerr << "Stavam sa utocnikom#############################" << endl;
            continue;
        }
        if(roles[i] == 1){ // 1 - Udrziavaj
            //ak nemas priradeny strom:
            if(lemurStrom[i].x == INT_MAX){
                //cerr << "hladam strom" << endl;
                lemurStrom[i] = najdiStrom(currlemur);
            }
            if(lemurStrom[i].x != INT_MAX){
                //cerr << "nasiel som na " << lemurStrom[i].x << ", " << lemurStrom[i].y << endl;
                Objekt TurbinaBlizko = nasaTurbina;
                commands[i] = Udrziavaj(currlemur, TurbinaBlizko, lemurStrom[i]);
            }
            else{
                commands[i] = Idluj(currlemur);
            }
        }
        else if(roles[i] == 2){ //2 - Minuj
            commands[i] = UtocnyMiner(currlemur);
            utocnyKeket = Objekt(currlemur.x,currlemur.y,TileType::TURBINE);
        }
        else if(roles[i] == 3){ //3 - Utoc
            commands[i] = Utocnik(currlemur, i);
        }
    }
        
    //cerr << world.players;
    //cerr << myself;
    currTah++;
    return commands;
}

//################################################################
//Hlavne funkcie


void init(){
    cerr<<world.height<<" "<<world.width<<endl;
    Player &myself = world.players[world.my_id];
    GetDosiahnutelne();
    cerr<<"done getdosiahnute"<<endl;
    GetCitronyGeneratory();
    cerr<<"done getcitronygeneratory"<<endl;
    findTurbines();
    cerr<<"done findTurbines"<<endl;
    for(auto i : StromyTurbiny[nasaTurbinaIndex]) cerr<<i.first.x<<" "<<i.first.y<<endl;
    for (int i = 0; i < myself.lemurs.size(); i++) {
        if(myself.lemurs[i].tools[0] == Tool::PICKAXE) roles.push_back(2);
        else roles.push_back(1);
        lemurStrom.push_back(Objekt());
        
    }
    cerr<<"Done init"<<endl;
}

int main() {
    // aby sme mali nahodu
    srand(time(nullptr));
    // povieme serveru ako sa chceme volat a farbu
    greet_server(NAME, COLOR);
    // robime tahy kym sme zivy
    bool first = true;
    do {
        cin >> world;
        if(first){
            init();
            first = 0;
        }
        send_commands(do_turn());
    } while (world.players[world.my_id].alive);
    cout << "Bye\n";
}

