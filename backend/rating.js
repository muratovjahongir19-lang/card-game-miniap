function updateElo(win,lose){


let k=32;


let expected=

1/

(1+

10**

((lose.elo-win.elo)/400)

);



win.elo += 
Math.round(
k*(1-expected)
);



lose.elo -=
Math.round(
k*(1-expected)
);



win.wins++;

lose.losses++;


}



module.exports={
updateElo
}
