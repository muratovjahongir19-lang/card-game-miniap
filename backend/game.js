const games={};


function createGame(room){


games[room]={

players:[],

bank:0,

turn:0,

cards:[

"A♠","K♠","Q♠",
"J♥","10♦","9♣"

]

};


return games[room];

}



function joinGame(room,player){


if(!games[room])
createGame(room);



games[room].players.push({

...player,

hand:[]

});



return games[room];

}



function dealCards(room){


let game=games[room];


game.players.forEach(player=>{


player.hand=[

game.cards[
Math.floor(
Math.random()*game.cards.length
)

],


game.cards[
Math.floor(
Math.random()*game.cards.length
)

]

];


});


return game;

}



function bet(room,playerId,amount){


let game=games[room];


game.bank+=amount;


return game;

}



function getWinner(room){


let game=games[room];


return game.players[
Math.floor(
Math.random()*game.players.length
)

];

}



module.exports={

createGame,

joinGame,

dealCards,

bet,

getWinner

};
