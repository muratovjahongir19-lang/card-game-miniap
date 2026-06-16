import React from "react";
import socket from "../socket";


export default function Emotes(){


const emojis=[

"😂",
"🔥",
"😎",
"👏",
"😡"

];


function send(e){

socket.emit(
"emotion",
e
);

}


return(

<div className="emotes">


{

emojis.map((e,i)=>(

<button
key={i}
onClick={()=>send(e)}
>

{e}

</button>


))

}


</div>


)

}
