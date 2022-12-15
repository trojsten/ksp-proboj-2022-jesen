#include "lemur.h"
#include <bits/stdc++.h>

using namespace std;

AdvancedLemur::AdvancedLemur(Lemur data, int id)
{
    this->data = data;
    this->id = id;
    // waitingForPickaxe = false;
}

AdvancedLemur::AdvancedLemur()
{
}

Command AdvancedLemur::Move(int turn)
{
    if (!data.alive)
    {
        cerr << "Dead" << endl;
        return NOOP();
    }
    // if (!hasTool(Tool::PICKAXE))
    // {
    //     if (waitingForPickaxe)
    //     {
    //         log("Waiting for pickaxe");
    //         return NOOP();
    //     }
    //     else
    //         waitingForPickaxe = false;
    // }
    if (!this->scheduled.empty())
    {
        Command cmd = this->scheduled.front();
        this->scheduled.pop();
        return cmd;
    }
    if (path.empty())
    {
        this->log("Requesting path");
        OnTurnRequest(turn, !path.empty());
    }
    if (!path.empty())
    {
        Point p = path.front();
        path.pop();
        pathSize = path.size();
        if (path.empty())
        {
            destination = Point(-1, -1);
            OnPathComplete(p);
        }
        else
        {
            log("Path size: " + to_string(path.size()));
            return MOVE(p.x, p.y);
        }
    }
    if (!this->scheduled.empty())
    {
        Command cmd = this->scheduled.front();
        this->scheduled.pop();
        return cmd;
    }
    log("Error: invalid state");
    return NOOP();
}

void AdvancedLemur::CancelMovement()
{
    queue<Point> empty;
    swap(this->path, empty);
}

void AdvancedLemur::MoveTo(vector<Point> path)
{
    destination = path[path.size() - 1];
    this->CancelMovement();
    pathSize = path.size();
    for (auto i : path)
    {
        this->path.push(i);
    }
}

void AdvancedLemur::Update(Lemur data)
{
    this->data = data;
}

void AdvancedLemur::OnTurnRequest(int turn, bool hasPath)
{
    log("Turn request");
}

void AdvancedLemur::OnPathComplete(Point dest)
{
    log("invalid function called");
}

bool AdvancedLemur::hasTool(Tool tool)
{
    for (auto i : data.tools)
    {
        if (i == tool)
            return true;
    }
    return false;
}

void AdvancedLemur::log(string msg)
{
    cerr << "[ lemur #" << id << " ]: " << msg << endl;
}

void AdvancedLemur::OnInitialize(Utils *u)
{
    util = u;
}