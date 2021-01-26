//
// Created by DOEMsy on 2021/1/2.
//

#include "UnitCard.h"


#include <utility>

UnitCard::UnitCard() {
    this->Type = CardTypeMonster;
    this->SelfCombat = 0;
}

UnitCard::UnitCard(const std::string &Name, const std::string &Desc, const int Combat, const int Level,
                   const std::set<label> &Label) : Card(Name, Desc) {
    this->Type = CardTypeMonster;
    this->SelfCombat = Combat;
    this->Level = Level;
    this->Label = Label;
}

//单位卡出牌动作为在目标位置召唤一个属性相同的随从
int UnitCard::Play(const int cardType, Player *player, int Card_i, std::vector<int> to) {
    //类型不一样 不合法 拒绝出牌
    if (cardType != this->Type) return 0;
    if (to[0] > 0) {
        //登场
        CopyCard(player->HandCards, Card_i, player->Lines[to[0]]);
        //执行登场效果
        Debut();
    } else if (to[0] < 0) {
        //登场
        CopyCard(player->OpPlayer->HandCards, Card_i, player->OpPlayer->Lines[to[0]]);
        //执行登场效果
        Debut();
    } else {

    }
    //出牌成功
    return 1;
}

int UnitCard::Combat() {
    int res = SelfCombat;
    for (auto &se : Status) {
        res += se.CombatAmend();
    }
    return res;
}






