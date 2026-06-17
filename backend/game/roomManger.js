const { createGame } = require("./durak");

const rooms = {};

function createRoom(roomId){

    rooms[roomId] = createGame();

    return rooms[roomId];
}

function getRoom(roomId){
    return rooms[roomId];
}

function addPlayer(roomId, player){

    if(!rooms[roomId]){
        createRoom(roomId);
    }

    rooms[roomId].players.push({
        id: player.id,
        name: player.name,
        hand: []
    });

    return rooms[roomId];
}

module.exports = {
    rooms,
    createRoom,
    getRoom,
    addPlayer
};
