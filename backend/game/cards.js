const suits = [
"♠",
"♥",
"♦",
"♣"
];

const ranks = [
"6",
"7",
"8",
"9",
"10",
"J",
"Q",
"K",
"A"
];

function createDeck(){

const deck=[];

for(const suit of suits){

for(const rank of ranks){

deck.push({
rank,
suit
});

}

}

return deck;

}

module.exports = {
createDeck
};
