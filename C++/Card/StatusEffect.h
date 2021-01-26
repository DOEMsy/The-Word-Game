//
// Created by DOEMsy on 2021/1/4.
//

#ifndef THE_WORD_GAME_STATUSEFFECT_H
#define THE_WORD_GAME_STATUSEFFECT_H


#include <string>
#include "../Game/Labels.h"

class StatusEffect {
private:
public:
    std::string Name;           //名称
    std::string Desc;           //描述
    int BasisCombatAmend = 0;   //基础战斗力修正
    std::set<attribute> Attrs;   //属性
    Card *ActingOnWho;          //作用于
    virtual int CombatAmend();          //战斗力修正值
};


#endif //THE_WORD_GAME_STATUSEFFECT_H
