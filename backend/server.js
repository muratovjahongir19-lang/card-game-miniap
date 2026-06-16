const express = require("express");

const {
createUser,
getUser
}=require("./database");
const cors = require("cors");
const http = require("http");

const {Server}=require("socket.io");


const app=express();

app.use(cors());


const server=http.createServer(app);


const io=new Server(server,{
cors:{
origin:"*"
}
});



let players=[];


let rooms={};

let user=createUser(player);

io.on("connection",(socket)=>{


console.log("Игрок подключился");



let player={

id:socket.id,

name:"Игрок_"+socket.id.slice(0,4),

money:25000

};


players.push(player);




io.emit(
"online",
players.length
);





socket.on(
"joinRoom",
(room)=>{


if(!rooms[room])
rooms[room]=[];



rooms[room].push(player);



socket.join(room);



io.to(room).emit(
"players",
rooms[room]
);



});






socket.on(
"message",
(data)=>{


io.emit(
"chat",
{

name:player.name,

text:data

}

);


});






socket.on(
"disconnect",
()=>{


players=
players.filter(
(p)=>p.id!==socket.id
);


io.emit(
"online",
players.length
);



});


});




app.get("/",(req,res)=>{

res.send(
"Card Game Server Online"
);

});



server.listen(3000,()=>{

console.log(
"Server started 3000"
);

});



socket.on(
"profile",
()=>{


socket.emit(
"profileData",
getUser(socket.id)
);


});
