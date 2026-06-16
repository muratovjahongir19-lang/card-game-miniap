const rooms={};


function createRoom(id,owner){


rooms[id]={

owner,

players:[],

private:true

};


return rooms[id];

}



function joinRoom(id,player){


if(rooms[id]){


rooms[id].players.push(player);


}


return rooms[id];

}



module.exports={

rooms,

createRoom,

joinRoom

};
