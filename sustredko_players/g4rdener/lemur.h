#ifndef LEMUR_H
#define LEMUR_H

#include "common.h"
#include <queue>
#include <vector>

struct Point
{
    int x;
    int y;

    Point(int y, int x) : x(x), y(y) {}
    Point()
    {
        x = -1;
        y = -1;
    }

    bool operator==(Point &a)
    {
        return x == a.x && y == a.y;
    }

    bool operator!=(Point &a)
    {
        return x != a.x || y != a.y;
    }
};

class Utils;

class AdvancedLemur
{
private:
    std::queue<Point> path;

protected:
    std::queue<Command> scheduled;
    void log(std::string msg);

public:
    Utils *util;
    Lemur data;
    Point destination;
    int pathSize;
    int id;
    bool waitingForPickaxe;
    bool hasTool(Tool tool);
    AdvancedLemur(Lemur data, int id);
    AdvancedLemur();
    Command Move(int turn);
    virtual void OnInitialize(Utils *u);
    virtual void OnTurnRequest(int turn, bool hasPath);
    virtual void OnPathComplete(Point dest);
    void CancelMovement();
    void MoveTo(std::vector<Point> path);
    void Update(Lemur data);
};

class Utils
{
private:
    World world;
    Lemur *IsLemur(Point p);
    AdvancedLemur *IsMyLemur(Point p);

public:
    Utils(World world);
    ~Utils();
    std::vector<AdvancedLemur *> lemury;
    std::vector<Point> GetPath(Point from, Point to);
    bool InGrid(int y, int x);
    bool IsOxygen(int y, int x);
    bool Empty(int y, int x);
    std::vector<Point> Closest(Point p, TileType typ);
    std::vector<Lemur *> ClosestLemur(Point p);
    std::vector<AdvancedLemur *> ClosestMyLemurs(Point p);
};

#endif