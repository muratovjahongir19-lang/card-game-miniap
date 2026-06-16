import React from "react";
import "./game.css";
import Deck from "../components/Deck";
import Timer from "../components/Timer";

export default function GameTable(){


const players=[
{
name:"Дмитрий",
money:1950,
avatar:"https://i.pravatar.cc/80?1"
},

{
name:"Виктория",
money:1800,
avatar:"https://i.pravatar.cc/80?2"
},

{
name:"Мария",
money:1700,
avatar:"https://i.pravatar.cc/80?3"
},

{
name:"Игорь_user",
money:2000,
avatar:"https://i.pravatar.cc/80?4"
}

];


return(

<div className="table-page">


<h2>
Комната #784512
</h2>


<div className="poker-table">



{
players.map((p,index)=>(

<div 
className={"player p"+index}
key={index}
>


<img src={p.avatar}/>


<div>

<b>{p.name}</b>

<p>
🪙 {p.money}
</p>

</div>


</div>

))

}



<div className="cards">


<div>A♠</div>

<div>K♥</div>

<div>7♦</div>

<div>3♣</div>


</div>



<div className="bank">

Банк
<br/>

1500 🪙

</div>


</div>



<div className="my-cards">


🂡 🂠

</div>


  <Timer/>

<Deck/>

<div className="actions">


<button className="fold">
Фолд
</button>


<button className="check">
Чек
</button>


<button className="bet">
Ставка 250$
</button>


<button className="raise">
Поднять
</button>



</div>



</div>


)

}
