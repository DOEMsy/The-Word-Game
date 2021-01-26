//
// Created by DOEMsy on 2021/1/5.
//

#ifndef THE_WORD_GAME_WOLF_H
#define THE_WORD_GAME_WOLF_H


#include "../../UnitCard.h"
class UnitCard;

class Wolf : public UnitCard {
private:
public:
    Wolf() : UnitCard(
            "狼",
            "森林中常见的野生动物",
            2,
            1,
            std::set<label>{
                    Animal,
            }
    ) {}
};


#endif //THE_WORD_GAME_WOLF_H
