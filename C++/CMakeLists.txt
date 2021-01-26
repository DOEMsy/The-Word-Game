cmake_minimum_required(VERSION 3.16)
project(The_Word_Game)

set(CMAKE_CXX_STANDARD 20)

add_executable(The_Word_Game main.cpp Game/Player.cpp Game/Player.h Card/Card.cpp Card/Card.h Card/UnitCard.cpp Card/UnitCard.h Game/Labels.h Game/Labels.cpp Game/Game.cpp Game/Game.h "Card/Original package/Original package.h" "Card/Original package/Unit/ImperialSoldier.h" Card/StatusEffect.cpp Card/StatusEffect.h "Card/Original package/Unit/Goblin.h" "Card/Original package/Unit/Wolf.h" ExternalLibrary/ExternalLibrary.cpp ExternalLibrary/ExternalLibrary.h)