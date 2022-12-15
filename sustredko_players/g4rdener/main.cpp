#include "common.h"
#include "Harvester.h"
#include "Attacker.h"
#include "lemur.h"

using namespace std;

#define NAME "Gardener"
#define COLOR "0d7516"

int DX[] = {0, 1, 0, -1};
int DY[] = {-1, 0, 1, 0};

World world;
vector<AdvancedLemur *> lemury;
int turn = 0;
int maxAttackers = 0;
int attackers;

AdvancedLemur *GetLemurType(Lemur lemur, Utils *u, int id)
{
    Point pos = Point(lemur.y, lemur.x);
    if (lemur.tools[0] == Tool::PICKAXE || lemur.tools[0] == Tool::PICKAXE && attackers < maxAttackers)
    {
        cerr << "Lemur has pickaxe" << endl;
        vector<Point> irons = u->Closest(pos, TileType::IRON);
        if (irons.size() > 0)
        {
            cerr << "Found closest iron" << endl;
            if (u->ClosestLemur(pos).size() > 0)
            {
                cerr << "Found target" << endl;
                attackers++;
                return new Attacker(lemur, id, u);
            }
        }
    }
    return new Harvester(lemur, id);
}

template <typename Base, typename T>
inline bool instanceof (const T *)
{
    return std::is_base_of<Base, T>::value;
}

void UpdateLemurType()
{
    int AttackerCount = 0;
    int HarvesterCount = 0;
    for (int i = 0; i < lemury.size(); i++)
    {
        if (instanceof <Attacker>(lemury[i]))
            AttackerCount++;
        else
            HarvesterCount++;
    }
}

// sem pis svoj kod
vector<Command> do_turn()
{
    Player &myself = world.players[world.my_id];
    Utils *u = new Utils(world);
    maxAttackers = myself.lemurs.size() / 2;
    if (turn == 0)
    {
        for (int i = 0; i < myself.lemurs.size(); i++)
        {
            Lemur lemur = myself.lemurs[i];
            lemury.push_back(GetLemurType(lemur, u, i));
        }
        u->lemury = lemury;
        for (auto lemur : lemury)
        {
            lemur->OnInitialize(u);
        }
    }
    vector<Command> commands;
    for (int i = 0; i < lemury.size(); i++)
    {
        lemury[i]->util = u;
        lemury[i]->Update(myself.lemurs[i]);
        commands.push_back(lemury[i]->Move(turn));
    }
    turn++;
    return commands;
}

int main()
{
    // aby sme mali nahodu
    srand(time(nullptr));
    // povieme serveru ako sa chceme volat a farbu
    greet_server(NAME, COLOR);
    // robime tahy kym sme zivy
    do
    {
        cin >> world;
        send_commands(do_turn());
    } while (world.players[world.my_id].alive);
    cout << "Bye\n";
}
