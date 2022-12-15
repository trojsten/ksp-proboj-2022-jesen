#include "Harvester.h"

using namespace std;

Harvester::Harvester(Lemur data, int id) : AdvancedLemur(data, id)
{
    log("Lemur is harvester");
}

Harvester::Harvester() : AdvancedLemur() {}

void Harvester::OnTurnRequest(int turn, bool hasPath)
{
    log("on turn request");
    Point pos = Point(data.y, data.x);
    if (data.lemon > 0)
    {
        log("finding turbine");
        vector<Point> turbines = util->Closest(pos, TileType::TURBINE);
        log("turbine found");
        auto path = util->GetPath(pos, turbines[0]);
        log("path generated");
        MoveTo(path);
    }
    else
    {
        log("finding tree");
        vector<Point> trees = util->Closest(pos, TileType::TREE);
        if (trees.size() > 0)
        {
            log("tree found");
            auto path = util->GetPath(pos, trees[0]);
            this->log("Path calculated, size " + to_string(path.size()));
            MoveTo(path);
        }
        else
        {
            vector<Point> path(1, Point(data.y, data.x));
            MoveTo(path);
        }
    }
}

void Harvester::OnPathComplete(Point dest)
{
    if (data.lemon > 0)
    {
        scheduled.push(PUT(dest.x, dest.y, InventorySlot::LEMON, 1));
    }
    else
    {
        scheduled.push(TAKE(dest.x, dest.y, InventorySlot::LEMON, 1));
    }
}