require("dotenv").config();

const express = require("express");
const cors = require("cors");
const http = require("http");
const { Server } = require("socket.io");

const {
    createUser,
    getUser
} = require("./database");

const {
    joinGame,
    dealCards,
    bet,
    getWinner
} = require("./game");

const app = express();

app.use(cors());
app.use(express.json());

const server = http.createServer(app);

const io = new Server(server,{
    cors:{
        origin:"*"
    }
});

const players = [];

io.on("connection",(socket)=>{

    console.log("Connected:",socket.id);

    const player = {

        id: socket.id,

        name: "Игрок_" + socket.id.slice(0,4),

        money: 25000

    };

    createUser(player);

    players.push(player);

    io.emit(
        "online",
        players.length
    );

    socket.on("profile",()=>{

        socket.emit(
            "profileData",
            getUser(socket.id)
        );

    });

    socket.on("joinGame",(room)=>{

        const game =
            joinGame(room,player);

        socket.join(room);

        io.to(room).emit(
            "gameUpdate",
            game
        );

    });

    socket.on("startGame",(room)=>{

        const game =
            dealCards(room);

        io.to(room).emit(
            "gameUpdate",
            game
        );

    });

    socket.on("bet",(data)=>{

        const game =
            bet(
                data.room,
                socket.id,
                data.amount
            );

        io.to(data.room).emit(
            "gameUpdate",
            game
        );

    });

    socket.on("message",(text)=>{

        io.emit(
            "chat",
            {
                name: player.name,
                text
            }
        );

    });

    socket.on("disconnect",()=>{

        const index =
            players.findIndex(
                p=>p.id===socket.id
            );

        if(index !== -1){

            players.splice(index,1);

        }

        io.emit(
            "online",
            players.length
        );

        console.log(
            "Disconnected:",
            socket.id
        );

    });

});

app.get("/",(req,res)=>{

    res.send(
        "Card Game Server Online"
    );

});

const PORT =
    process.env.PORT || 3000;

server.listen(PORT,()=>{

    console.log(
        "Server started on port",
        PORT
    );

});
