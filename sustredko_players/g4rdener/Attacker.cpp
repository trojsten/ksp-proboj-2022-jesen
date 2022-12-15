#include "Attacker.h"
#include <bits/stdc++.h>

using namespace std;

Attacker::Attacker(Lemur data, int id, Utils *u) : AdvancedLemur(data, id)
{
    givingPickaxe = NULL;
}

void Attacker::OnInitialize(Utils *u)
{
    AdvancedLemur::OnInitialize(u);
    this->log("Lemur is attacker");
    Point pos = Point(data.y, data.x);
    vector<Point> iron = u->Closest(pos, TileType::IRON);
    MoveTo(u->GetPath(pos, iron[0]));
}

Attacker::Attacker() : AdvancedLemur() {}

void Attacker::OnPathComplete(Point pos)
{
    log("Completed path");
    // if (givingPickaxe != NULL)
    // {
    //     log("giving pickaxe");
    //     for (int i = 0; i < givingPickaxe->pathSize; i++)
    //     {
    //         log("giving pickaxe 2");
    //         this->scheduled.push(NOOP());
    //     }
    //     this->scheduled.push(PUT(pos.x, pos.y, InventorySlot::TOOL1, 1));
    //     log("Giving pickaxe to lemur #" + to_string(givingPickaxe->id));
    //     vector<Point> iron = util->Closest(pos, TileType::IRON);
    //     MoveTo(util->GetPath(Point(data.x, data.y), iron[0]));
    // }
    if (hasTool(Tool::KNIFE))
    {
        log("Stab");
        this->scheduled.push(STAB(pos.x, pos.y));
    }
    else
    {
        log("break");
        this->scheduled.push(BREAK(pos.x, pos.y));
        if (data.iron == 1)
        {
            this->scheduled.push(CRAFT(Tool::KNIFE));
        }
    }
}

void Attacker::OnTurnRequest(int turn, bool hasPath)
{
    this->log("Has knife: " + to_string(hasTool(Tool::KNIFE)));
    Point pos = Point(data.y, data.x);
    vector<Lemur *> targets = util->ClosestLemur(pos);
    vector<Point> completePath = util->GetPath(pos, Point(targets[0]->y, targets[0]->x));
    vector<Point> path(std::min((int)completePath.size(), 3), Point(-1, -1));
    for (int i = 0; i < path.size(); i++)
    {
        path[i] = completePath[i];
    }

    this->log("Moving to " + to_string(pos.x) + "," + to_string(pos.y));
    MoveTo(path);
    if (hasTool(Tool::KNIFE))
    {
    }
    else
    {
        // if (data.stone < 2)
        // {
        //     vector<Point> stone = util->Closest(Point(data.y, data.x), TileType::STONE);
        //     MoveTo(util->GetPath(Point(data.y, data.x), stone[0]));
        // }
        // if (data.stone == 2)
        // {
        //     this->scheduled.push(CRAFT(Tool::PICKAXE));
        //     vector<AdvancedLemur *> l = util->ClosestMyLemurs(Point(data.y, data.x));
        //     int minDist = INT32_MAX;
        //     AdvancedLemur *t;
        //     for (auto lemur : l)
        //     {
        //         if (lemur->hasTool(Tool::PICKAXE))
        //             continue;
        //         Point target = lemur->destination == Point(-1, -1) ? Point(lemur->data.y, lemur->data.x) : lemur->destination;
        //         int dist = abs(target.x - data.x) + abs(target.y - data.y);
        //         if (dist < minDist)
        //         {
        //             minDist = dist;
        //             t = lemur;
        //         }
        //     }
        //     t->waitingForPickaxe = true;
        //     givingPickaxe = t;
        //     vector<Point> path = util->GetPath(Point(data.y, data.x), t->destination);
        //     MoveTo(path);
        // }
    }
}