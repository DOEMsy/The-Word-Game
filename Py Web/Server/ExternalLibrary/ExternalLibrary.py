# 全局变量
from copy import deepcopy
from random import choice, sample

GlobalVariable = dict()


# 设定全局变量
def GloSet(key, value):
    GlobalVariable[key] = value


# 获取全局变量
def GloGet(key):
    return GlobalVariable.get(key)


# 将卡组中的卡全部转换成字典
def toDict(Cards: []) -> list:
    res = []
    for card in Cards:
        res.append(card.dict())
    return res

# 将卡组中的卡全部转换成长字符串
def toLstr(Cards: []) -> list:
    res = []
    for card in Cards:
        res.append(card.lstr())
    return res

# 将卡组中的卡打包
def PackList(Cards: []) -> list:
    res = []
    for card in Cards:
        res.append(card.pack())
    return res

def GetAllCardLstrList() ->list:
    return toLstr(AllCard)

# 全部的卡包
AllCard = []

# 查询全集
AllSearchCard = dict()
AllSearchCard["Level"] = dict()
AllSearchCard["Label"] = dict()
AllSearchCard["Type"] = dict()


# 注册卡
def RegistrationCard(*Cards):
    for insert_value in Cards:
        # 使得卡在列入牌库的时候就具有UID
        # 但是抽卡，或从牌库直接获取卡牌的时候，仍然需要使用 ConcretizationCard 函数，防止多次使用 GetCardSet 出现UID一样的卡牌
        # 首先 GetCardSet 的设计原则是保证，在单次抽卡内的卡是各不相同的，但是多次使用 GetCardSet 可以在不同次中出现相同的卡
        # 获取从 GetCardSet 中获取的卡牌或者直接从原卡牌生成的卡牌，必须使用 ConcretizationCard ，防止 UID 冲突
        # print("加载卡牌：",insert_value)
        card = ConcretizationCard(insert_value)
        AllCard.append(card)

        # 预处理类型
        try:
            type = card.Type
            try:
                AllSearchCard["Type"][type].add(card)
            except:
                AllSearchCard["Type"][type] = set()
                AllSearchCard["Type"][type].add(card)
        except:
            pass

        # 预处理等级
        try:
            level = card.Level
            try:
                AllSearchCard["Level"][level].add(card)
            except:
                AllSearchCard["Level"][level] = set()
                AllSearchCard["Level"][level].add(card)
        except:
            pass

        # 预处理标签
        try:
            labels = card.Label
            for lab in labels:
                try:
                    AllSearchCard["Label"][lab].add(card)
                except:
                    AllSearchCard["Label"][lab] = set()
                    AllSearchCard["Label"][lab].add(card)
        except:
            pass


# 求卡集
#   PropertyRequirements = {
#       "Type" : str,
#       "Level": num,
#       "Label": set
#   }
def GetCardSet(PropertyRequirements: dict):
    res = set()
    for key, value in PropertyRequirements.items():
        try:
            if(key=="Label"):
                for lb in value:
                    if (len(res) == 0):
                        res = AllSearchCard[key][lb]
                    else:
                        res = res & AllSearchCard[key][lb]
            else:
                if (len(res) == 0):
                    res = AllSearchCard[key][value]
                else:
                    res = res & AllSearchCard[key][value]
        except:
            pass
    return list(res)


# 求随机卡（弃用）
# def GetRandCard(PropertyRequirements: dict, num: int):
#     res = []
#     cs = GetCardSet(PropertyRequirements)
#     for i in range(num):
#         res.append(ConcretizationCard(choice(cs)))
#     return res


# 求随机卡，允许需要重复卡的重复
# 返回的是原肧卡，需要具象化才能使用
def GetRandCard(PropertyRequirements: dict, num: int):
    res = []
    cs = GetCardSet(PropertyRequirements)
    try:
        res = sample(cs, min(len(cs), num))
    except:
        pass

    return res


# 全局UID
GloUID = 15363


# 分配UID
def GetUID():
    global GloUID
    GloUID += 1
    return GloUID


# 常量
# 不施法标识，对于任何选定型技能，使用这个表示该技能打空
NoSpell = -15442
# 错误标识，表示存在错误输入
IsError = -48481


def INT(inp):
    try:
        return int(inp)
    except:
        if (inp == "none"):
            return NoSpell
        else:
            return IsError


# 具象化卡牌，完全复制一份一模一样但是UID不同的卡牌
def ConcretizationCard(*cards):
    if(len(cards)==1):

        p,g = cards[0].OwnPlayer,cards[0].ThisGame
        cards[0].OwnPlayer = None
        cards[0].ThisGame = None  # 本局游戏

        res = deepcopy(cards[0])
        res.UID = GetUID()
        res.visualization = True

        res.OwnPlayer,res.ThisGame = cards[0].OwnPlayer,cards[0].ThisGame = p,g
        return res
    else:
        res = []
        for card in cards:
            p, g = card.OwnPlayer, card.ThisGame
            card.OwnPlayer = None
            card.ThisGame = None  # 本局游戏

            tmp = deepcopy(card)
            tmp.UID = GetUID()
            tmp.visualization = True

            tmp.OwnPlayer, tmp.ThisGame = card.OwnPlayer, card.ThisGame = p, g

            res.append(tmp)
        return res

# 抛出异常，具象化错误
# 卡牌在具象化之前被使用了
def Throw_VisualizationError(card):
    print("错误！卡牌",card,"在具象化之前被使用了")
    error = 1/0
