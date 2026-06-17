const {createDeck}=require("./cards");
const shuffle=require("./shuffle");

function createGame(){

const deck=
shuffle(
createDeck()
);

const trump=
deck[
deck.length-1
];

return{

deck,

trump,

players:[],

table:[],

turn:0

};

}

module.exports={
createGame
};


function deal(game){

game.players.forEach(player=>{

while(
player.hand.length<6 &&
game.deck.length>0
){

player.hand.push(
game.deck.pop()
);

}

});

}
