const { createDeck } = require("./cards");
const shuffle = require("./shuffle");

function createGame(){

    const deck = shuffle(createDeck());

    const trumpCard = deck[deck.length - 1];

    return {

        deck,

        trump: trumpCard,

        players: [],

        attacker: 0,

        defender: 1,

        table: [],

        started: false

    };
}

function dealCards(game){

    game.players.forEach(player=>{

        while(
            player.hand.length < 6 &&
            game.deck.length > 0
        ){
            player.hand.push(
                game.deck.pop()
            );
        }

    });

    return game;
}

module.exports = {
    createGame,
    dealCards
};
