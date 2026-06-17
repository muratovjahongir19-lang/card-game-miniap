const values = {

"6":0,
"7":1,
"8":2,
"9":3,
"10":4,
"J":5,
"Q":6,
"K":7,
"A":8

};

function canBeat(
attack,
defense,
trumpSuit
){

if(
attack.suit === defense.suit
){

return (
values[defense.rank]
>
values[attack.rank]
);

}

if(
defense.suit === trumpSuit &&
attack.suit !== trumpSuit
){

return true;

}

return false;

}

module.exports = {
canBeat
};
