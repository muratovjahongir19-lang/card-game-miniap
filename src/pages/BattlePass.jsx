import React,{useState} from "react";

export default function BattlePass(){

const [level,setLevel]=useState(1);

const [xp,setXp]=useState(0);

function addXp(){

let newXp=xp+25;

if(newXp>=100){

setLevel(level+1);
setXp(0);

}else{

setXp(newXp);

}

}

return(

<div className="card">

<h1>🎫 Battle Pass</h1>

<h2>Уровень {level}</h2>

<p>XP: {xp}/100</p>

<button onClick={addXp}>
Получить XP
</button>

</div>

);

}
