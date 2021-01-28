//import net from 'net';
var net = require('net')

var comSocket = net.Socket();
var scrSocket = net.Socket();

comSocket.connect({
    host: '192.168.1.101',
    port: 27015
})

scrSocket.connect({
    host: '192.168.1.101',
    port: 27016
})


// 接收数据
comSocket.on('data', function (data) {
    //console.log(data.toString());
})

// 接收数据
scrSocket.on('data', function (data) {
    console.log(JSON.parse(data.toString())['scr']);
})
