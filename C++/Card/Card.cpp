//
// Created by DOEMsy on 2021/1/2.
//

#include "Card.h"

Card::Card() {
    this->Type = CardTypeNULL;
}

Card::Card(const std::string &Name, const std::string &Desc) {
    this->Name = Name;
    this->Desc = Desc;
    this->Type = CardTypeNULL;
}

Card::~Card() {

}


