//
// Created by DOEMsy on 2021/1/2.
//

#ifndef THE_WORD_GAME_UNITCARD_H
#define THE_WORD_GAME_UNITCARD_H

#include <set>
#include "Card.h"
#include "../Game/Player.h"
#include "../Game/Labels.h"

class Card;
class Player;

class UnitCard : public Card {
private:
public:

    int SelfCombat;                     //战斗力
    int Level;                          //级别
    std::set<label> Label;              //标签
    std::vector<StatusEffect> Status;    //状态效果

    UnitCard();

    UnitCard(const std::string &Name, const std::string &Desc, const int Combat, const int Level,
             const std::set<int> &Label);

    virtual int Play(const int cardType, Player *player, int Card_i, const std::vector<int> to);

    virtual int Combat();

    virtual int Debut() { return 1 };
};


#endif //THE_WORD_GAME_UNITCARD_H
