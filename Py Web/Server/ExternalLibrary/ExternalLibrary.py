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

# 全部的卡包
AllCard = []

# 查询全集
AllSearchCard = dict()
AllSearchCard["Level"] = dict()
AllSearchCard["Label"] = dict()
AllSearchCard["Type"] = dict()


# 注册卡
def RegistrationCard(Cards: list):
    for card in Cards:
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
#       "Type" :[],
#       "Level":[],
#       "Label":[]
#   }
def GetCardSet(PropertyRequirements: dict):
    res = set()
    for key, value in PropertyRequirements.items():
        try:
            if (len(res) == 0):
                res = AllSearchCard[key][value]
            else:
                res = res & AllSearchCard[key][value]
        except:
            pass
    return list(res)


# 求随机卡
def GetRandCard(PropertyRequirements: dict, num: int):
    res = []
    cs = GetCardSet(PropertyRequirements)
    for i in range(num):
        res.append(deepcopy(choice(cs)))
    return res

# 求随机卡，不重复
def GetRandUnrepeatCard(PropertyRequirements: dict, num: int):
    res = []
    cs = GetCardSet(PropertyRequirements)
    try:
        res = sample(cs,min(len(cs),num))
    except:
        pass

    return res


#全局UID
GloUID = 15363

#分配UID
def GetUID():
    global GloUID
    GloUID += 1
    return GloUID

#常量
#不施法标识，对于任何选定型技能，使用这个表示该技能打空
NoSpell = -15442