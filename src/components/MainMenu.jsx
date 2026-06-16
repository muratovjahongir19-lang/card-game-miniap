import React from "react";


export default function MainMenu({setPage}){


return(

<div className="menu">


<h1>
🎴 CARD GAME
</h1>


<div className="money">

🪙 25000
💎 350

</div>



<button
onClick={()=>setPage("game")}
>

⚔️ Играть

</button>



<button>

🏆 Турниры

</button>



<button>

🛒 Магазин

</button>



<button>

👥 Друзья

</button>



</div>

)

}
