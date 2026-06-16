import React from "react";

import socket from "../socket";


export default function Actions(){


function send(action){


socket.emit(
"move",
{

room:"room1",

action:action,

players:4

}

);


}



return(

<div>


<button onClick={()=>send("fold")}>

❌ Пас

</button>



<button onClick={()=>send("check")}>

✅ Чек

</button>



<button onClick={()=>send("bet")}>

🪙 Ставка

</button>



</div>

)

}
