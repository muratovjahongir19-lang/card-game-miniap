import React,{useEffect,useState} from "react";

import socket from "../socket";


export default function Game(){


const [game,setGame]=useState(null);



useEffect(()=>{


socket.emit(
"joinGame",
"room1"
);



socket.on(
"gameUpdate",
(data)=>{


setGame(data);


});


},[]);



function start(){


socket.emit(
"startGame",
"room1"
);


}



function bet(){


socket.emit(
"bet",
{

room:"room1",

amount:100

}

);


}



return(

<div className="card">


<h1>
🎴 Игра
</h1>



<button onClick={start}>
Раздать карты
</button>


<button onClick={bet}>
Ставка 100
</button>



{

game &&

<div>


<h2>
Банк: {game.bank}
</h2>



{

game.players.map((p,i)=>(

<p key={i}>

👤 {p.name}

{

p.hand.map((c)=>

<span>
 {c}
</span>

)

}

</p>

))

}


</div>


}



</div>

)

  }
