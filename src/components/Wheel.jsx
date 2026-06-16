import React,{useState} from "react";


export default function Wheel(){


const [reward,setReward]=useState("");



function spin(){


let prizes=[

"500 🪙",

"1000 🪙",

"VIP день",

"Сундук 🎁",

"10000 🪙"

];


let r=

prizes[
Math.floor(
Math.random()*prizes.length
)

];


setReward(r);


}



return(

<div className="card">


<h2>
🎡 Колесо удачи
</h2>


<div className="wheel">

🎡

</div>


<button onClick={spin}>

Крутить

</button>


<h3>
{reward}
</h3>


</div>


)

}
