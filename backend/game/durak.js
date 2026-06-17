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
