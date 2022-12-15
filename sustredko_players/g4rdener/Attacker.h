#ifndef ATTACKER_H
#define ATTACKER_H

#include "lemur.h"

class Attacker : public AdvancedLemur
{
private:
    AdvancedLemur *givingPickaxe;

public:
    Attacker(Lemur data, int id, Utils *u);
    Attacker();
    void OnInitialize(Utils *util) override;
    void OnPathComplete(Point pos) override;
    void OnTurnRequest(int turn, bool hasPath) override;
};

#endif