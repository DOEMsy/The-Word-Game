//
// Created by DOEMsy on 2021/1/2.
//

#ifndef THE_WORD_GAME_GAME_H
#define THE_WORD_GAME_GAME_H

#include <vector>
#include "Player.h"
class Player;

#define DAY 0
#define NIGHT 1

class Game {
private:
public:
    Player Players[2];   //玩家
    cardDeck GlobalEffect;  //全球效果
    cardDeck PlayCardQueue;
    bool DayOrNight;    //昼夜
    int NumberOfBoard;  //场数

    Game();
    int SettlementToNextTurn(); //场替
    int SettlementRound();      //结算轮
    int DeathDetection();       //检测死亡
    int CalculateCombat();      //计算战斗力

    int PrintScreen(int NO);    //打印界面
    int GetAndCROInstructions(int NO);  //获取并执行指令
};


#endif //THE_WORD_GAME_GAME_H
