#include <iostream>
#include "Game/Player.h"
#include "Game/Game.h"
#include "Card/Original package/Original package.h"

int main() {
    Game Game;
    bool woFirst = rand()%2;

    //test ↓

    for(int i=0;i<20;i++) {
        Game.Players[0].RawPile.push_back(Goblin());
        Game.Players[0].RawPile.push_back(ImperialSoldier());
        Game.Players[1].RawPile.push_back(Goblin());
        Game.Players[1].RawPile.push_back(ImperialSoldier());
    }
    //test ↑

    while(Game.NumberOfBoard<3){
        Player &FirstPlayer = Game.Players[woFirst];
        Player &SecondPlayer = Game.Players[!woFirst];
        while(!FirstPlayer.IsAbstain or !SecondPlayer.IsAbstain){
            if(!FirstPlayer.IsAbstain){
                //先手出牌
                Game.PrintScreen(FirstPlayer.NO);
                Game.GetAndCROInstructions(FirstPlayer.NO);
                //发动效果

            //结算回合，包括死亡检测
                //先手玩家发动场上技能
                FirstPlayer.SettlementOnCourtSkill();
                //死亡检测
                Game.DeathDetection();
                //重新计算双方战斗力
                Game.CalculateCombat();
            }
            if(!SecondPlayer.IsAbstain){
                //后手出牌
                Game.PrintScreen(SecondPlayer.NO);
                Game.GetAndCROInstructions(SecondPlayer.NO);
                //发动效果

            //结算回合，包括死亡检测
                //后手玩家发动场上技能
                SecondPlayer.SettlementOnCourtSkill();
                //死亡检测
                Game.DeathDetection();
                //重新计算双方战斗力
                Game.CalculateCombat();
            }
            //结算轮
            Game.SettlementRound();
        }
        Game.SettlementToNextTurn();
    }
    return 0;
}

