import React,{useState} from "react";


export default function Admin(){


const [players,setPlayers]=useState(1250);



return(

<div className="card">


<h1>
⚙️ Admin Panel
</h1>


<p>
Игроков онлайн: {players}
</p>


<button
onClick={()=>
setPlayers(players+1)
}
>

Добавить игрока

</button>



<button>

Заблокировать читера

</button>


</div>

)

}
