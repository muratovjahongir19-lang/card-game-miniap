import React from "react";


export default function History(){


const games=[

{
enemy:"Player_123",
result:"Победа",
coins:"+500"
},

{
enemy:"Player_777",
result:"Поражение",
coins:"-250"
}

];


return(

<div className="card">


<h1>
📜 История игр
</h1>


{

games.map((g,i)=>(

<div key={i}
className="game">

<p>
🎴 Против: {g.enemy}
</p>

<p>
{g.result}
</p>

<p>
🪙 {g.coins}
</p>

</div>

))

}



</div>

)

}
