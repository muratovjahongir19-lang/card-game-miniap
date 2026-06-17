const { createMatch, dealCards } =
require("./durakEngine");

const matches = {};

function startMatch(room){

    const match =
    createMatch();

    dealCards(match);

    matches[room] = match;

    return match;
}

function getMatch(room){
    return matches[room];
}

module.exports = {
    startMatch,
    getMatch
};
