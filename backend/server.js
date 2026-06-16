const express = require("express");

const {
createTurn,
nextTurn,
tick
}=require("./turn");

const {
joinGame,
dealCards,
bet,
getWinner
}=require("./game");

const {
checkPlayer
}=require("./anticheat");

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
  
if(!checkPlayer(player)){

socket.disconnect();

}


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

  socket.on(
"joinGame",
(room)=>{


let game=
joinGame(room,player);


socket.join(room);

  socket.on(
"startGame",
(room)=>{

socket.on(
"startGame",
(room)=>{


let game=
dealCards(room);


createTurn(room);


io.to(room)
.emit(
"gameUpdate",
game
);


});

  socket.on(
"move",
(data)=>{


let turn=
nextTurn(
data.room,
data.players
);


io.to(data.room)
.emit(
"turn",
turn
);


});


let game=
dealCards(room);


io.to(room).emit(
"gameUpdate",
game
);


});

socket.on(
"bet",
(data)=>{


let game=
bet(
data.room,
socket.id,
data.amount
);



io.to(data.room)
.emit(
"gameUpdate",
game
);



});


io.to(room).emit(
"gameUpdate",
game
);


});



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


socket.on(
"tableChat",
(msg)=>{


io.emit(
"tableChat",
msg
);


});
