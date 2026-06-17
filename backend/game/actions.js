const {
canBeat
}=require("./cardPower");


function attack(
match,
playerIndex,
card
){

if(
playerIndex !==
match.attacker
){

return false;

}

match.table.push({

attack:card,

defense:null

});

return true;

}



function defend(
match,
playerIndex,
card
){

if(
playerIndex !==
match.defender
){

return false;

}

const pair =
match.table.find(
x=>x.defense===null
);

if(!pair)
return false;


if(

canBeat(
pair.attack,
card,
match.trump.suit
)

){

pair.defense = card;

return true;

}

return false;

}

module.exports = {

attack,

defend

};
