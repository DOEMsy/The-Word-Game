namespace py game
namespace go game
namespace cpp game

struct Base{
    1: i64 status_code,
    2: string status_message,
    3: i64 cnt,
}

struct Req{
    1: i64 player_NO,
    2: string ins,
    3: optional list<string> para, // ins参数

    255: optional Base base,
}

struct Resp{
    1: i64 player_NO,
    2: string ins,
    3: optional string screen, // 屏幕
    4: optional string msg,    // 推送消息

    255: optional Base base,
}

service GameServer {
    Resp what_should_I_do(1:Req req), // 主服务，指导c/s同步
    Resp get_msg(1:Req req),          // 获取实时推送
}

