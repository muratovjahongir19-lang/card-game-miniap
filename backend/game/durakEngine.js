const suits = ["♠","♥","♦","♣"];

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

    const deck = [];

    for(const suit of suits){

        for(const rank of ranks){

            deck.push({
                suit,
                rank
            });

        }

    }

    return deck;
}

function shuffle(deck){

    for(let i=deck.length-1;i>0;i--){

        const j =
        Math.floor(
            Math.random()*(i+1)
        );

        [deck[i],deck[j]] =
        [deck[j],deck[i]];
    }

    return deck;
}

function createMatch(){

    const deck =
    shuffle(createDeck());

    const trump =
    deck[deck.length-1];

    return {

        deck,

        trump,

        players:[],

        table:[],

        attacker:0,

        defender:1,

        started:false

    };

}

function dealCards(match){

    match.players.forEach(player=>{

        while(
            player.hand.length < 6 &&
            match.deck.length > 0
        ){

            player.hand.push(
                match.deck.pop()
            );

        }

    });

    return match;
}

module.exports = {

    createMatch,

    dealCards

};
