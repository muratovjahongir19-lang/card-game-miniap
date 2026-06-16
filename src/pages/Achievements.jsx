import React from "react";


export default function Achievements(){


const items=[

"🥇 Первая победа",

"🎴 100 игр",

"🏆 Турнирный чемпион",

"💎 VIP игрок"

];


return(

<div className="card">


<h1>
🏅 Достижения
</h1>


{

items.map((x,i)=>(

<p key={i}>
{x}
</p>

))

}


</div>

)

}
