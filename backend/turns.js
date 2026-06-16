const turns={};


function createTurn(room){

turns[room]={

player:0,

time:15

};

return turns[room];

}



function nextTurn(room,total){


if(!turns[room])
createTurn(room);


turns[room].player++;


if(turns[room].player>=total){

turns[room].player=0;

}


turns[room].time=15;


return turns[room];

}



function tick(room){


if(turns[room]){

turns[room].time--;

}


return turns[room];

}



module.exports={
createTurn,
nextTurn,
tick
};
