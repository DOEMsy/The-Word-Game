//
// Created by DOEMsy on 2021/1/2.
//

#include "Player.h"

#include <utility>

int TransferCard(cardDeck &from,int pos,cardDeck &to){
    to.push_back(from[pos]);
    from.erase(from.begin()+pos);
}

int CopyCard(cardDeck &from,int pos,cardDeck &to){
    to.push_back(from[pos]);
}

int GetRoundPos(int size){
    return rand()%size;
}

Player::Player() = default;

Player::Player(std::string Name, int NO) {
    this->Name = std::move(Name);
    this->NO = NO;
    this->Health = 3;
    this->TolCombat = 0;
    this->IsAbstain = false;
}

int Player::SettlementOnCourtSkill() {
    for(auto &Line:Lines){
        for(auto &Unit:Line){
            Unit.OnCourt();
        }
    }
    return 1;
}

//ins = pair(CardType,To[])
int Player::PopCard(int Card_i, const instruction & ins) {

    //超出卡牌数组，拒绝出牌
    if(this->HandCards.size()<=Card_i)  return 0;
    //卡牌类型不同，拒绝出牌
    if(this->HandCards[Card_i].Type!=ins.first) return 0;

    auto &cardType = ins.first;
    auto &to = ins.second;

    if(this->HandCards[Card_i].Play(cardType, this, Card_i, to)){
        TransferCard(HandCards,Card_i,ThisGame->PlayCardQueue);
        return 1;   //合法出牌
    }else{
        return 0;   //不合法拒绝出牌
    }
}


int Player::GetCard(int Card_num) {
    int i = 0;
    int RawPileSize = this->RawPile.size();
    for(;i<Card_num&&RawPileSize>0;i++){
        int p = GetRoundPos(RawPileSize);
        TransferCard(this->RawPile,p,this->HandCards);
        RawPileSize--;
    }
    return i;   //返回实际抽牌数
}

int Player::ThrowCard(int Card_i) {
    //超出范围拒绝扔牌
    if(Card_i > HandCards.size()-1) return 0;
    else {
        HandCards.erase(HandCards.begin() + Card_i);
        return 1;
    }
}

int Player::ThrowCards(std::vector<int> Card_is) {

    //去重+排序
    std::set<int>s(Card_is.begin(),Card_is.end());
    Card_is.assign(s.begin(),s.end());

    //超出范围拒绝扔牌
    if(*Card_is.rbegin()>HandCards.size()-1) return 0;
    else {
        Card_is.size();
        for(int i = 0;i<Card_is.size();i++){
            HandCards.erase(HandCards.begin()+Card_is[i]-i);
        }
        return 1;
    }
}

int Player::CalculateCombat() {
    this->TolCombat = 0;
    for(auto &Line:Lines){
        for(auto &Card:Line){
            if(Card.Type==CardTypeMonster){
                this->TolCombat += Card.Combat();
            }
        }
    }
    return 1;
}



