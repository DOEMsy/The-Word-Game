//
// Created by DOEMsy on 2021/1/5.
//

#ifndef THE_WORD_GAME_GOBLIN_H
#define THE_WORD_GAME_GOBLIN_H

#include "../../UnitCard.h"
class UnitCard;

class Goblin : public UnitCard{
private:
public:
    Goblin() : UnitCard(
            "哥布林",
            "小型的野生哥布林，是一种常见的魔物",
            2,
            1,
            std::set<label>{
                    Humanoid,
            }
    ) {}
};


#endif //THE_WORD_GAME_GOBLIN_H
