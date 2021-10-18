## 开发日记

* 2021.1.25
  * 近期目标
    * [x] 将玩家1从服务端分离
    * [x] 改使用 json 传输信息
    * [x] 制定 json 规则	
    * [x] 手造消息队列
    * [x] 协程轮询接收 socket 消息
  
* 2021.1.26
  * 加入 TCP 消息缓冲队列
  * 重构三层出牌函数
  * TCP 传输改用 Json 数据包
  
* 2021.1.27
  * 制定 json 传输规则
  * 近期目标：
    * [ ] 完善Mod开发手册
    * [ ] 完善客户端开发手册
    * [x] 实现技能卡牌相关功能
  
* 2021.1.28
  * 补充通信规则
  * 近期目标：
    * [x] 实现技能卡牌相关功能
      * [x] 完善事件系统（事件驱动模型 ）
        * [x] 公共监视器
        * [x] 独立监视器
  
* 2021.1.29
  
  * 设计架构，为事件系统做准备
  
* 2021.1.30
  * 大量重构架构
  * 初步完成公共监视器
  * 完成死亡监视器
  
* 2021.1.31
  * 事件以及监视器系统完成
  * 近期目标
    * [ ] 完善Mod开发手册
      * [x] 普通单位卡
      * [x] 带触发的单位卡
      * [x] 技能卡
      * [x] 带召唤的技能卡
  
* 2021.2.9
  * 再次大规模重构，以适应后续的技能实现
  * 改进了抽牌算法，保证不会出现重复卡牌
  
* 2021.2.10
  * 修复单位被施加BUFF游戏中断的bug
  * 加入了东方Project相关的卡包扩展
  
* 2021.2.11
  * 修复了部分卡牌的bug
  * 添加心跳包保证服务器支持长连接
  * 优化了主进程等待逻辑，保证事件处理完成之前不会抢占资源
  
* 2021.2.12
  
  * 临时添加了消息系统
  
* 2021.2.14
  
  * 修改了牌库机制，允许需要卡牌重复，但是视为不同卡牌
  
* 2021.3.11

  * 再版通信规则，移植部分逻辑到客户端

  

  

## 服务端数据通信规则 *v0.5.0*

服务器开放有两个端口 指令通信端口 和 屏幕通信端口

> 两个玩家共用一套通信端口，但拥有各自独立的通信Channel

### 异步线程通信（屏幕通信）

* 开始游戏信息

  * 对局信息
    * 对局模式
    * 双方玩家信息

  ```json
  {
      "ins":"game_start",
      "mode":"normal",
   	"players":[
          {
              "NO":"0",
              "Name":"玩家1",
              "Desc":"座右铭1",
              "Health":2,
          },{
              "NO":"1",
              "Name":"玩家2",
              "Desc":"座右铭2",
          	"Health":2,
          }
      ]
  }
  ```

  

* 卡牌变动

  * 己方加牌（S）
    * 牌信息
      * 牌类型（给位置-单位，不给位置-技能）
      * 卡牌技能 指定单位
        * 数量
        * 是否可空
      * 卡牌技能 指定行
        * 数量
        * 是否可空
      * 待定
      * 内容负责指示 出牌操作

  **技能牌**

  ```python
  {
      "ins":"card_pump",
      "card":{
          "Name":"name",
          "Desc":"desc",
          "Type":"SkillCard",
          "Label":["label"],
          "OwnNO":0,
          "Level":0,
      	"UID":"UID",
          
          # 释放目标需求，[选目标数，必须选全，选行数目，必须选全]
         	"UnleashOp":[0,False,0,False],
          # 需要选择多少张牌进行献祭，（随机献祭不算在内）
          "SelDedication":0,
      },
  }
  ```

  **单位牌**

  ```python
  {
  	"ins":"card_pump",
  	"card":{
  		"Name":"name",
          "Desc":"desc",
          "Type":"UnitCard",
          "Label":["label"],
          "OwnNO":0,
          "Level":0,
      	"UID":"UID",
          # 能够放置的行
          "CantoLines":[1,2,3],
         	"SelfCombat":0,
          "Combat":0,
          "Status":[
              StatusEffect1,
              StatusEffect2,
              StatusEffect3,
          ]
          # 释放目标需求，[选目标数，必须选全，选行数目，必须选全]
         	"UnleashOp":[0,fasle,0,fasle],
          # 需要选择多少张牌进行献祭，（随机献祭不算在内）
          "SelDedication":0,
  	}
  }
  ```

  其中 StatusEffect 内容为

  ```python
  {
      "Name":"name",
      "Desc":"desc",
      "UID":"UID",
      "Type":"StatusEffect",
      # 效果类型 0：未知，1：战斗力增益，2：战斗力减益，3：护盾
      "Effect":0,
      # 作用效果值
      "Value":0,
      "Label":["label"]
  }
  ```

  

  * 更新卡牌信息（S）

    * 卡牌上场

    ```python
    {
        "ins":"card_to_line",
    	"card":UnitCard,
        "To":1,
    }
    ```
    
  * 卡牌基础战斗力增加
    
  ```python
    {
    	"ins":"card_add_combat",
        "para":{
            "UID":"UID",
            "Value":0,
        }
  }
  ```

    * 卡牌受伤

    ```python
    {
    	"ins":"card_get_damage",
        "para":{
            "UID":"UID",
            "Value":0,
        }
    }
    ```

    * 卡牌描述变化
      * 效果变化（状态效果变化）
      
      **效果施加**
      
      ```python
      {
          "ins":"card_effect_add",
          "card":{
              "Name":"name",
              "Desc":"desc",
              "UID":"UID",
              "Type":"StatusEffect",
              # 效果类型 0：未知，1：战斗力增益，2：战斗力减益，3：护盾
              "Effect":0,
              # 作用效果值
              "Value":0,
              "Label":["label"]
          }
      }
      ```
      
      **效果消除**
      
      ```python
      {
          "ins":"card_effect_del",
          "para":{
              "CardUID":"cardUID",
          	"StauUID":"stauUID",
          }
      }
      ```
      
      **效果变化**
      
      ```python
      {
          "ins":"card_effect_value_change",
          "para":{
              "CardUID":"cardUID",
          	"StauUID":"stauUID",
              # 可省略参数
              "Name":"change_name",
              "Desc":"change_desc",
              "Label":"change_label",
              "Value":0,
              "Label":["label"],
          }
      }
      ```
      
      * 描述变化
      
      ```Python
      {
          "ins":"card_change",
          "para":{
              "UID":"UID",
              # 可省略参数
              "Name":"change_name",
              "Desc":"change_desc",
              "Label":["label"],
              "Level":"change_level",
              "SelfCombat":0,
          }
      }
      ```
      
    * 卡牌退场
      * 单位死亡
      
      ```python
      {
          "ins":"card_dead",
          "para":{
              "UID":"UID",
          }
      }
      ```
      
      * 单位场替
      
      ```python
      {
          "ins":"card_selturn",
          "para":{
              "UID":"UID",
          }
      }
      ```
      
    * 卡牌位置变化

    ```python
    {
        "ins":"card_selturn",
        "para":{
            "UID":"UID",
            # 目标行 -3 -2 -1 1 2 3
            "To":1,
        }
    }
    ```

    * 弃牌

    ```python
    {
    	"ins":"card_throw",
    	"para":{
    		"ThrowList":[
    			"UID1",
    			"UID2",
    			"UID3",
    			...
    		]
    	}
    }
    ```

* 玩家变化（S）

  * 墓地数量变化

  ```python
  {
      "ins":"player_unitGraveSize_change",
  	"para":{
  		"PlayerNO":0,
  		"Change":0,
      }
  }
  ```

  * 抽牌堆数量变化

  ```python
  {
      "ins":"player_rawPileSize_change",
  	"para":{
  		"PlayerNO":0,
  		"Change":0,
      }
  }
  ```

  * 玩家名称变化

  ```python
  {
      "ins":"player_name_change",
  	"para":{
  		"PlayerNO":0,
  		"Change":"name",
      }
  }
  ```

* 对局变化（S）

  * 对局信息变化
    * 场替

      * 场次
      * 胜负

      ```python
      {
          "ins":"game_toNextInnings",
      	"para":{
      		"WinerNO":0,
          }
      }
      ```

    * 全局效果

      **效果施加**

      ```python
      {
          "ins":"game_effect_add",
          "card":{
              "Name":"name",
              "Desc":"desc",
              "Type":"SkillCard",
              "Label":["label"],
              "Level":0,
          	"UID":"UID",
          }
      }
      ```

      **效果消除**

      ```python
      {
          "ins":"game_effect_del",
          "para":{
          	"UID":"UID",
          }
      }
      ```

      **效果变化**

      ```python
      {
          "ins":"game_effect_value_change",
          "para":{
              "UID":"UID",
              # 可省略参数
              "Name":"change_name",
              "Desc":"change_desc",
              "Label":["label"],
              "Level":"change_level",
          }
      }
      ```

    * ~~双方战斗力~~

      ```python
      {
          
      }
      ```

* 消息提示（S）

```python
{
    "ins":"prt",
    "para":{
        "msg":"message",
    }
}
```

### 主线程通信（指令通信）

* 玩家行动（C）
  
  * 出牌
  
  ```python
  {
      "ins":"pop",
      "para":{
          "card_i":0,
          "card_uid":"UID",
          "card_type":"type",
          "to":0,
          "targetUIDs":[],
          "targetLines":[],
          "selDedicUIDs":[],
      }
  }
  ```
  
  * 放弃
  
  ```python
  {
  	"ins":"giveup",
  	"para":{
  	
  	}
  }
  ```
  
* 行动指示（S）

  * 请出牌

  ```python
  {
      "ins":"inp",
      "para":{
          "msg":"",
          "ct":0,
      }
  }
  ```

  

## 单位卡战斗力

单位卡战斗力分为 **基础值(SelfCombat)​** 和 **应用值(Combat)​** ，单位拥有一个 ​**状态槽(Status)​** 

* 状态槽​，表示单位目前身上拥有的状态组成的队列，每个状态都可能有一些作用效果
* 基础值，表示单位在无状态条件下，纯粹自身的战力值
* 应用值，表示单位的 **基础值​** 加上身上 ​**状态槽** 中所有作用效果后得到的战力值，应用值不能低于 $0$ 



## 单位的死亡判定

当单位的 **基础值** 战斗力为 $0$ 时候，进入**濒死状态**，此时单位的 **应用值** 为 $0$，无视 **状态槽** 加成。

当单位的 **基础值** 战斗力小于 $0$ 时，死亡，移入墓地。

