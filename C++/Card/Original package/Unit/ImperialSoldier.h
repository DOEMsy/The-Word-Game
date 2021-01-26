//
// Created by DOEMsy on 2021/1/4.
//

#ifndef THE_WORD_GAME_IMPERIALSOLDIER_H
#define THE_WORD_GAME_IMPERIALSOLDIER_H

#include "../../UnitCard.h"
class UnitCard;

class ImperialSoldier : public UnitCard {
private:
public:
    ImperialSoldier() : UnitCard(
            "帝国士兵",
            "一名普普通通的士兵，本本分分的谋生",
            3,
            1,
            std::set<label>{
                    Humanoid,
            }
    ) {}
};


#endif //THE_WORD_GAME_IMPERIALSOLDIER_H
