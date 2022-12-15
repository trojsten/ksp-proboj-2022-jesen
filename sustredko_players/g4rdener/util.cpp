#include <vector>
#include "lemur.h"

using namespace std;

int dirX[4] = {1, -1, 0, 0};
int dirY[4] = {0, 0, 1, -1};

Utils::Utils(World world)
{
    this->world = world;
}

vector<Point> Utils::GetPath(Point from, Point to)
{
    queue<pair<Point, Point>> rad;
    rad.push({from, Point(-1, -1)});
    vector<vector<Point>> skade(world.height, vector<Point>(world.width, Point(-1, -1)));

    while (!rad.empty())
    {
        auto x = rad.front();
        Point p = x.first;
        Point prev = x.second;
        rad.pop();
        if (skade[p.y][p.x] != Point(-1, -1))
            continue;
        skade[p.y][p.x] = prev;
        if (p == to)
        {
            deque<Point> path;
            Point a = p;
            while (a != from)
            {
                path.push_front(a);
                a = skade[a.y][a.x];
            }
            vector<Point> out;
            for (auto i : path)
            {
                out.push_back(i);
            }
            return out;
        }
        for (int i = 0; i < 4; i++)
        {
            if (InGrid(p.y + dirY[i], p.x + dirX[i]) && skade[p.y + dirY[i]][p.x + dirX[i]].x == -1)
            {
                if (Point(p.y + dirY[i], p.x + dirX[i]) == to)
                    rad.push({Point(p.y + dirY[i], p.x + dirX[i]), p});
                if (Empty(p.y + dirY[i], p.x + dirX[i]) && IsOxygen(p.y + dirY[i], p.x + dirX[i]))
                    rad.push({Point(p.y + dirY[i], p.x + dirX[i]), p});
            }
        }
    }

    return vector<Point>(1, from);
}

bool Utils::InGrid(int y, int x)
{
    bool b = x >= 0 && x < world.width && y >= 0 && y < world.height;
    return b;
}

bool Utils::IsOxygen(int y, int x)
{
    return world.oxygen[y][x] > 0;
}

bool Utils::Empty(int y, int x)
{
    bool b = world.tiles[y][x].type == TileType::EMPTY;
    return b;
}

vector<Point> Utils::Closest(Point p, TileType typ)
{
    // world.players[0].lemurs
    cerr << "Finding closest" << endl;
    vector<vector<bool>> visited(world.height, vector<bool>(world.width, false));
    std::queue<Point> rad;
    rad.push(p);
    visited[p.y][p.x] = true;
    vector<Point> res;
    while (!rad.empty())
    {
        Point q = rad.front();
        rad.pop();
        for (int i = 0; i < 4; i++)
        {
            if (InGrid(q.y + dirY[i], q.x + dirX[i]) && !visited[q.y + dirY[i]][q.x + dirX[i]])
            {
                if (world.tiles[q.y + dirY[i]][q.x + dirX[i]].type == typ)
                {
                    res.push_back(Point(q.y + dirY[i], q.x + dirX[i]));
                    cerr << "Found type" << res.size() << endl;
                }
                if (Empty(q.y + dirY[i], q.x + dirX[i]) && IsOxygen(q.y + dirY[i], q.x + dirX[i]))
                {
                    cerr << "Add to queue" << endl;
                    rad.push(Point(q.y + dirY[i], q.x + dirX[i]));
                    visited[q.y + dirY[i]][q.x + dirX[i]] = true;
                }
            }
        }
    }
    return res;
}

vector<Lemur *> Utils::ClosestLemur(Point p)
{
    vector<Lemur *> res;
    vector<vector<bool>> visited(world.height, vector<bool>(world.width, false));
    std::queue<Point> rad;
    rad.push(p);
    visited[p.y][p.x] = true;
    while (!rad.empty())
    {
        Point q = rad.front();
        rad.pop();
        for (int i = 0; i < 4; i++)
        {
            if (InGrid(q.y + dirY[i], q.x + dirX[i]) && !visited[q.y + dirY[i]][q.x + dirX[i]])
            {
                Lemur *lemur = IsLemur(Point(q.y + dirY[i], q.x + dirX[i]));
                if (lemur != nullptr)
                    res.push_back(lemur);

                if (Empty(q.y + dirY[i], q.x + dirX[i]) && IsOxygen(q.y + dirY[i], q.x + dirX[i]))
                {
                    rad.push(Point(q.y + dirY[i], q.x + dirX[i]));
                    visited[q.y + dirY[i]][q.x + dirX[i]] = true;
                }
            }
        }
    }

    sort(
        res.begin(), res.end(), [p](Lemur *&a, Lemur *&b)
        { 
            int scoreA = abs(p.x - a->x) + abs(p.y - a->y); 
            if(a->tools[0] == Tool::KNIFE || a->tools[1] == Tool::KNIFE)
                scoreA += 20;
            int scoreB = abs(p.x - b->x) + abs(p.y - b->y); 
            if(b->tools[0] == Tool::KNIFE || b->tools[1] == Tool::KNIFE)
                scoreB += 20;
            return scoreA < scoreB; });
    return res;
}

// std::vector<AdvancedLemur *> Utils::ClosestMyLemurs(Point p)
// {
//     vector<AdvancedLemur *> res;
//     vector<vector<bool>> visited(world.height, vector<bool>(world.width, false));
//     std::queue<Point> rad;
//     rad.push(p);
//     visited[p.y][p.x] = true;
//     while (!rad.empty())
//     {
//         Point q = rad.front();
//         rad.pop();
//         for (int i = 0; i < 4; i++)
//         {
//             if (InGrid(q.y + dirY[i], q.x + dirX[i]) && !visited[q.y + dirY[i]][q.x + dirX[i]])
//             {
//                 AdvancedLemur *l = IsMyLemur(Point(q.y + dirY[i], q.x + dirX[i]));
//                 if (l != nullptr)
//                     res.push_back(l);

//                 if (Empty(q.y + dirY[i], q.x + dirX[i]) && IsOxygen(q.y + dirY[i], q.x + dirX[i]))
//                 {
//                     rad.push(Point(q.y + dirY[i], q.x + dirX[i]));
//                     visited[q.y + dirY[i]][q.x + dirX[i]] = true;
//                 }
//             }
//         }
//     }
//     return res;
// }

Lemur *Utils::IsLemur(Point p)
{
    for (int i = 0; i < this->world.players.size(); i++)
    {
        if (world.players[i].id == world.my_id)
            continue;
        for (int j = 0; j < world.players[i].lemurs.size(); j++)
        {
            if (!world.players[i].lemurs[j].alive)
                continue;
            if (p == Point(world.players[i].lemurs[j].y, world.players[i].lemurs[j].x))
                return &world.players[i].lemurs[j];
        }
    }
    return nullptr;
}

// AdvancedLemur *Utils::IsMyLemur(Point p)
// {
//     for (int i = 0; i < lemury.size(); i++)
//     {
//         if (lemury[i]->data.y == p.y && lemury[i]->data.x == p.x)
//             return lemury[i];
//     }
//     return nullptr;
// }