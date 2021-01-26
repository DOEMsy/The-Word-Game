//
// Created by DOEMsy on 2021/1/2.
//

#ifndef THE_WORD_GAME_CARD_H
#define THE_WORD_GAME_CARD_H

#include<string>
#include "../Game/Labels.h"

#define CardTypeNULL 0          //空类型卡
#define CardTypeMonster 1       //单位类型卡
#define CardTypeSkill 2         //技能类型卡

class Card {
private:
public:
    std::string Name;           //名称
    std::string Desc;           //描述
    int Type;                   //类型

    int SelfCombat;             //战斗力
    int Level;                  //级别
    std::set<label> Label;      //标签
    std::vector<StatusEffect> Status;    //状态效果

    Card();

    Card(const std::string &Name, const std::string &Desc);

    virtual int Combat() { return 1; };

    virtual int Play(const int i, Player *pPlayer, int Card_i, const std::vector<int> vector) { return 1 };     //出牌效果
    virtual int OnHand() { return 1; };   //持有效果
    virtual int Aban() { return 1; };     //弃牌效果

    virtual int Debut() { return 1; };        //登场
    virtual int OnCourt() { return 1; };      //每一玩家回合结束时
    virtual int ToNextTurn() { return 1; };   //场替
    virtual int Dead() { return 1; };         //死亡

    virtual int Round() { return 1; };        //每一轮结束时
    virtual int Finish() { return 1; };      //是否消耗殆尽

    ~Card();
};


#endif //THE_WORD_GAME_CARD_H
