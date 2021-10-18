# DEMO（待定名）

这是一个类昆特牌的双人对战游戏，支持跨平台互联网联机、自建卡牌mod。

目前只实现了主要游戏逻辑，支持断线重连、事件触发器、卡牌接口。

游戏操作/界面暂时很不友好，技术力有限、无限期鸽置。

## 快速开始

**运行环境**

* python 3.6+

**克隆代码库**

```C++
git clone https://github.com/SAU-OSSA/The-Word-Game.git
```

**安装运行库**

```
pip install thrift
```



## 开始游戏

**启动服务器**

* 默认开启本地服务器，可以在 ``Server.Game.Game.Host`` 中修改

```
cd 'Py Web'
python ./Server/main.py
```

**启动客户端**

* 默认连接本地服务器，可以在 `Client.main.GameClient.host` 中修改
* 连接两个玩家后游戏开始

```
python ./Client/main.py
NO 0 or 1 ？ # 选择玩家0 or 1
```

**客户端断线重连**

* 重新启动客户端



## How to play?

**出牌** 

```
pop <手牌序号> [目标行] [目标id] [弃牌序号]
# <必选> [附加]
```

**放弃出牌**

```
giveup
```



## 扩展接口

目前高度集成了卡牌接口，可以在数十行内快速实现一些有趣的卡牌逻辑，包括事件触发、出牌效果、光环效果等，甚至不需要考虑卡牌退场时各种技能效果/触发器的回收。

下面只介绍一部分基本接口，更多模板参考 `Server.Mod.OriginalPackage`

#### 怎么写一个单位牌？

1. 继承基类 `Server.Card.UnitCard`

2. 基础属性（必写）

```python
class Wolf(UnitCard):
    def __init__(self):
        super().__init__(
            name="狼",	# 名称
            desc="森林中常见的野生动物",	# 说明文字
            combat=2,	# 基础战斗力 >=0
            level=1,	# 等级 [1,2,3,4,5]
            label={		# 标签（参考Server.Game.Label,支持自定义）
                "动物",
            },
            canto={1},	# 可以出牌的行 [-3,-2,-1,1,2,3],负数为对方战场
        )
```

3. 注册卡牌

```Python
# Server.Mod.OriginalPackage.__init__

from Mod.OriginalPackage import Unit
from Mod.OriginalPackage import Skill
from ExternalLibrary.ExternalLibrary import RegistrationCard
RegistrationCard(
    *4 * [Unit.Wolf()], # 向牌库中塞入4张狼
)
```

#### 怎么写一个单位牌？（进阶）

可以通过重写接口实现各种炫酷的技能。

##### 出牌效果

* 卡牌从手牌中打出的效果 

```Python
# UnitCard._deubt(self,ins) -> bool:
# 	ins: pop所有[附加]指令参数
#	return: 出牌是否合法，False将不可出牌
#	函数将会在出牌时执行
class Doppler(UnitCard):
    def _debut(self, ins) -> bool:
        try:
            if (ins[1] != NoSpell):
                card = self.ThisGame.UIDCardDict[ins[1]]
                self.Name = card.Name + "（变形怪）"
                self.SelfCombat = card.SelfCombat
                self.Label = deepcopy(card.Label)
                self.Level = card.Level
            return True
        except:
            return False
        
# 可以在出牌效果中对目标施加某些状态魔法 or 造成伤害
class DobbyGolem(UnitCard):
    def _debut(self, ins) -> bool:
        if (choice([True, False])):
            self.AddStatus(self.effect)
        return True
    
class GiantMalu(UnitCard):
    def _debut(self, ins) -> bool:
        self.ThisGame.UIDCardDict[ins[1]].GetDamage(randint(self.min_dmg, self.max_dmg), {"物理"})
        return True
```

##### 持续效果

* 卡牌登场效果

```Python
# 考虑到卡牌可能会不经过手牌打出
# def UnitCard._selftoLineOn(self) -> bool:
#	return: 一定返回True,没有含义
#	函数将会在卡牌登场执行
class Deusexmachina(UnitCard):
    def _selftoLineOn(self) -> bool:
        for card in self.OwnPlayer.UIDCardDict.values():
            if (card.UID != self.UID):
                card.AddShield(self.shield_give, {"机械"})
		return True
    
# 有一种特殊的登场效果，为自身施加效果可以不用重写接口
# self.Effect 中的效果出场自动施加
class BigWolf(UnitCard):
   	def __init__(self):
    	self.Effect = [Effect.Nocturnal(self.night_combat_add), ]
```

* 光环效果

```python
# 卡牌在场上时可以用光环影响其他人
class DemonJay(UnitCard):
    def __init__(self):
    	self.ExiEffectOn = [-3, -2, -1, 1, 2, 3] # 影响范围
    	self.ExiLabel = {"魔法", "恶魔"}	# 效果label
    
    # def UnitCard._exiEffect(self,target)
    # 	target：影响目标(UnitCard)
    #   return: 返回对目标的战斗力影响值，注意这里一定要返回值
    def _exiEffect(self, target):
        if (Is("普通生物", target) or Is("高等生物", target)):
            return -self.exisEffectCmt
        else:
            return 0

# 同时每一个单位都有一个响应光环影响的接口
class WuZun(UnitCard):
    # def UnitCard._combat_exis_effect(self,effect)
    # 	effect：影响来源（UnitCard) 
    #	return：返回对该效果影响的响应值，注意这里一定要返回值
    def _combat_exis_effect(self, effect) -> int:
        res, label = effect.ExiEffect(self) # 获取光环的影响值和label
        if (res < 0): res *= (1 - self.debuf_off) # 自适应调整
        return res	# 返回最终影响值
```

* 事件触发

```python
# 样例
class Ghoul(UnitCard):
    def __init__(self):
         # 注册死亡触发器
        self.Monitor_Death = True
        
	def _deathProcessing(self, event):
        # 检测到别人死亡时战斗力增加
        UID = event['para'][0]
        if (UID != self.UID):
            # self.SelfCombat += self.skill_carrion_increased_combat
            self.AddSelfCombat(self.skill_carrion_increased_combat, {"特性"})

# 单位卡拥有三种触发器接口：
    self.Monitor_Death = False  # 死亡监视器
    self.Monitor_Pop = False  # 出牌监视器
    self.Monitor_GetDmg = False  # 单位受伤监视器
  	# 触发器接口为 True 时，卡牌登场时会注册至全局触发器容器
    
# 发生对应事件会执行触发器
    # 死亡触发器，event = {'type':'Death','para':[UID,UnitCard]}
    # UID: 死亡卡牌uid
    # UnitCard：死亡卡牌
    def _deathProcessing(self, event):
        return True
    
    # 出牌触发器，event = {'type':'Pop','para':[PlayerNO,Card]}
    # PlayerNO：出牌玩家编号
    # Card：打出的牌
    def _popProcessing(self, event):
        return True
    
    # 受伤触发器，event = {'type':'GetDmg','para':[UID,attack_res,cureDmg,UnitCard]}
    # attack_res：0免疫 1受伤 2受伤且死亡
    # cureDmg：实际攻击伤害
    def _getDmgProcessing(self, event):
        return True

```

* 其他

```python
# 受到攻击，扣血并返回伤害数值，0 表示免疫了伤害
# 可以重写实现伤害减免，受伤释放技能等
def _getDamage(self, num, effectLabel):
    self.SelfCombat -= num # 扣血
    return num

# 受到回复，回复并返回回血数值，0 表示免疫了效果
# 可以重写实现回复量调整，回复释放技能等
def _addSelfCombat(self, num, effectLabel):
    self.SelfCombat += num
    return num

# 是否可以死亡，返回False可以免疫死亡
def _dead(self) -> bool:
    return True

# 同理还有护盾
def _addShield(self, num, label):
    self.ShieldValue += num
    return num

def _devShield(self, num, label):
    sdmg = min(self.ShieldValue, num)
    self.ShieldValue -= sdmg
    return sdmg
```

##### 单位技能

```python
# 考虑实现一种主动技能机制，区别于出场效果，只要卡牌存活时，可以随时释放。
# ComCard = {SkillCard:card_num,...}
# 单位出场后玩家会获得 ComCard 中的所有法术牌，这些牌和该单位是绑定的
# 只要该单位存活，可以随时释放这些法术牌
# 但是当其死亡时，所有与其绑定的未释放法术牌会被强制弃牌
class DeadSage(UnitCard):
    def __init__(self):
        self.ComCard = {Skill.TheFlameofBoredom(): self.card_num}
```



#### 怎么写一个法术牌？

1. 继承基类 `Server.Card.SkillCard`

```python
# 实现法术牌非常简单，常用接口只有出牌效果 _debut
class Explosion(SkillCard):
    def __init__(self):
        self.minDamage = 0
        self.maxDamage = 16
        super().__init__(
            name="爆裂魔法",
            desc="某红魔大法师的招牌魔法，对敌方所有单位造成{}-{}点魔法伤害\n"
                 "Explosion~!"
                 "".format(self.minDamage, self.maxDamage),
            level=4,
            label={
                "魔法"
            }
        )

    # 与单位牌的 _debut 使用方法基本相同
    def _debut(self, ins) -> bool:
        for card in self.OwnPlayer.OpPlayer.UIDCardDict.values():
            card.GetDamage(
                randint(self.minDamage, self.maxDamage),
                self.Label
            )
        return True

```

2. 注册卡牌

```python
# Server.Mod.OriginalPackage.__init__

from Mod.OriginalPackage import Unit
from Mod.OriginalPackage import Skill
from ExternalLibrary.ExternalLibrary import RegistrationCard
RegistrationCard(
    *1 * [Skill.Explosion()], # 向牌库中塞入1张爆裂魔法
)
```

