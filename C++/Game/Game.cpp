//
// Created by DOEMsy on 2021/1/2.
//

#include <iostream>
#include "Game.h"
#include "../ExternalLibrary/ExternalLibrary.h"

Game::Game() {
    this->Players[0] = Player("Player1", 0);
    this->Players[1] = Player("Player2", 1);
    this->Players[0].OpPlayer = &Players[1];
    this->Players[1].OpPlayer = &Players[0];
    this->Players[0].ThisGame = this->Players[1].ThisGame = this;
    this->DayOrNight = rand() % 2;
    this->NumberOfBoard = 0;
}

int Game::SettlementToNextTurn() {

    //战斗力低的一方扣血
    if (Players[0].TolCombat < Players[1].TolCombat) {
        Players[0].Health--;
    } else if (Players[0].TolCombat > Players[1].TolCombat) {
        Players[1].Health--;
    } else {
        Players[0].Health--;
        Players[1].Health--;
    }

    //场替
    for (auto &Player : this->Players) {
        for (auto &Line : Player.Lines) {
            for (auto &Unit : Line) {
                if (Unit.ToNextTurn()) {
                    delete &Unit;
                }
            }
        }
    }

    for (auto &Card:this->GlobalEffect) {
        if (Card.ToNextTurn()) {
            delete &Card;
        }
    }

    //下一场
    this->NumberOfBoard++;
    DayOrNight = !DayOrNight;
    Players[0].IsAbstain = Players[1].IsAbstain = false;

    return 1;
}

int Game::DeathDetection() {
    for (auto &Player : this->Players) {
        for (auto &Line : Player.Lines) {
            for (auto &Unit : Line) {
                if (Unit.Combat() <= 0 && Unit.Dead()) {
                    Player.UnitGrave.push_back(Unit);
                    delete &Unit;
                }
            }
        }
    }
    return 1;
}

int Game::SettlementRound() {
    for (auto &Effect: this->GlobalEffect) {
        Effect.Round();
        if (Effect.Finish()) {
            delete &Effect;
        }
    }
    return 1;
}

int Game::CalculateCombat() {
    Players[0].CalculateCombat();
    Players[1].CalculateCombat();
    return 1;
}

int Game::PrintScreen(int NO) {
    auto &Player = Players[NO];
    auto &OpPlayer = *Player.OpPlayer;
    //打印对方战场
    for (int i = 2; i >= 0; i--) {
        printf("%d: ", &i);
        for (auto &Card : OpPlayer.Lines[i])
            printf("[%s,%d,%d],", Card.Name.c_str(), Card.Combat(), Card.Level);
        printf("\n");
    }
    printf("-----------NA:%d CO:%d, HE:%d ----------\n", OpPlayer.Name, OpPlayer.TolCombat, OpPlayer.Health);
    //打印全图效果
    printf("%s\n", (DayOrNight ? "Day" : "Night"));
    printf("GL: ");
    for (auto &Card : GlobalEffect) {
        printf("[%s],", Card.Name.c_str());
    }
    printf("\n");
    //打印己方战场
    printf("-----------NA:%d CO:%d, HE:%d ----------\n", Player.Name, Player.TolCombat, Player.Health);
    for (int i = 0; i <= 2; i++) {
        printf("%d: ", &i);
        for (auto &Card : Player.Lines[i])
            printf("[%s,%d,%d],", Card.Name.c_str(), Card.Combat(), Card.Level);
        printf("\n");
    }

    //打印手牌
    printf("\nHandCard:\n");
    int Card_i = 0;
    for (auto &Card:Player.HandCards) {
        printf("%d. [%s,%d,%d,%s]\n", ++Card_i, &Card.Name, Card.Combat(), &Card.Level, Card.Desc);
    }

    return 1;
}

int Game::GetAndCROInstructions(int NO) {
    std::string inp;
    while (std::cin >> inp) {
        auto ins = ExternalLibrary::SPLIT(inp);
        //ins "  "
        if (ins[0] == "giveup") {
            //ins = "giveup"
            //弃权
            Players[NO].IsAbstain = true;
            break;
        } else if (ins[0] == "pop") {
            //ins = "pop card_i card_type to[]"
            //出牌
            int card_i = ExternalLibrary::INT(ins[1]);
            int card_type = ExternalLibrary::INT(ins[2]);
            auto to = ExternalLibrary::INT(ExternalLibrary::SUBVEC(ins, 3));
            if (Players[NO].PopCard(card_i, instruction(card_type, to))) {
                //出牌成功
                break;
            } else {
                //出牌不合法
            }
        } else if (ins[0] == "get") {
            //ins = "get card_num"
            int card_num = ExternalLibrary::INT(ins[1]);
            Players[NO].GetCard(card_num);
        }
        ExternalLibrary::LOG("指令不合法，请重新输入：");
    }

    return 1;
}
