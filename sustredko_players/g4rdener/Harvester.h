#ifndef HARVESTER_H
#define HARVESTER_H

#include "lemur.h"

class Harvester : public AdvancedLemur
{
private:
public:
    Harvester(Lemur data, int id);
    Harvester();
    void OnTurnRequest(int turn, bool hasPath) override;
    void OnPathComplete(Point dest) override;
};

#endif