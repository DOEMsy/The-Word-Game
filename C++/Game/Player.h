//
// Created by DOEMsy on 2021/1/2.
//

#ifndef THE_WORD_GAME_PLAYER_H
#define THE_WORD_GAME_PLAYER_H

#include "Game.h"
#include "../Card/Card.h"
#include <vector>

class Game;
class Card;

#define ints std::vector<int>
#define instruction std::pair<int,std::vector<int> >
#define cardDeck std::vector<Card>

//转移卡牌
int TransferCard(cardDeck &from,int pos,cardDeck &to);
//复制卡牌
int CopyCard(cardDeck &from,int pos,cardDeck &to);
//得到一个随机的卡牌位置
int GetRoundPos(int size);

class Player {
private:
public:
    cardDeck HandCards; //手牌
    cardDeck RawPile;  //抽牌堆
    cardDeck UnitGrave; //坟墓

    #define FRO 0   //前线
    #define MID 1   //中场
    #define SUP 2   //支援
    cardDeck Lines[3];  //战线

    bool IsAbstain; //是否弃权

    std::string Name;           //昵称
    int NO;         //编号
    int Health;     //生命值
    int TolCombat;  //战力值和
    Player  *OpPlayer;    //指向对手
    Game    *ThisGame;  //指向本游戏

    Player();
    Player(std::string Name,int NO);

    int PopCard(int Card_i,const instruction& ins);        //出牌
    int GetCard(int Card_num);      //抽牌
    int ThrowCard(int Card_i);      //弃牌
    int ThrowCards(ints Card_is);    //弃牌

    int SettlementOnCourtSkill();   //结算回合技能
    int CalculateCombat();          //计算战斗力
};


#endif //THE_WORD_GAME_PLAYER_H
