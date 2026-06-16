import React,{useState} from "react";


const cards=[
"A♠","K♠","Q♠","J♠",
"A♥","K♥","Q♥","J♥",
"A♦","K♦","Q♦","J♦",
"A♣","K♣","Q♣","J♣"
];


export default function Deck(){

const [hand,setHand]=useState([]);


function deal(){

let random=[...cards]
.sort(()=>Math.random()-0.5)
.slice(0,2);

setHand(random);

}


return(

<div>


<button
onClick={deal}
className="deal"
>
Раздать карты
</button>


<div className="hand">

{

hand.map((c,i)=>(

<div key={i}
className="card"
>

{c}

</div>

))

}

</div>


</div>

)

}
