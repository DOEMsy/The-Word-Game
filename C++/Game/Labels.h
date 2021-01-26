//
// Created by DOEMsy on 2021/1/2.
//



#ifndef THE_WORD_GAME_LABELS_H
#define THE_WORD_GAME_LABELS_H

#include "../Card/UnitCard.h"
#include "../Card/StatusEffect.h"

class UnitCard;
class StatusEffect;

#define label int
#define attribute label

/* 单位标签 */

bool Is(label, const UnitCard&);

//普通生物 OrdinaryCreatures
#define OrdinaryCreatures 100
#define Humanoid    101   //人类、亚人
#define Animal      102   //动物

//不死者 UndeadCreatures
#define UndeadCreatures 200
#define Vampire     201   //血族
#define Undead      202   //亡灵

//高等生物 AdvancedCreature
#define AdvancedCreature 300
#define Natural     301     //自然
#define Dragon      302     //龙
#define Mechanical  303     //机械
#define MagicCreature 304   //魔法生物

//彼世 OutsideWorldCreature
#define OutsideWorldCreature 400
#define Demon   401     //恶魔
#define Apostle 402     //天使
#define Deity   403     //神明
#define Corrupt 404     //腐化

/* 技能属性 */

bool Is(attribute, const StatusEffect&);

#define Sacred      1       //神圣
#define Corrupted   2       //腐化
#define Magical     3       //魔法
#define Physical    4       //物理

#endif //THE_WORD_GAME_LABELS_H
