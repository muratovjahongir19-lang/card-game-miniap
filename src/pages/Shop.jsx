import React,{useState} from "react";


export default function Shop(){


const [coins,setCoins]=useState(25000);

const [vip,setVip]=useState(false);



function bonus(){

setCoins(
coins+1000
);

alert(
"+1000 монет за вход!"
);

}



function buyVip(){

setVip(true);

alert(
"VIP активирован!"
);

}



return(

<div className="card">


<h1>
🛒 Магазин
</h1>



<h2>
🪙 {coins}
</h2>



<button onClick={bonus}>

🎁 Ежедневный бонус +1000

</button>



<button onClick={buyVip}>

💎 Купить VIP

</button>



{

vip &&

<h3>
⭐ VIP игрок
</h3>

}




<div>

<h2>
🎫 Battle Pass
</h2>


<p>
Уровень: 1/50
</p>


<button>

Открыть награду

</button>


</div>



</div>

)

}
