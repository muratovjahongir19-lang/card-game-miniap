import { useState } from "react";
import GameTable from "./pages/GameTable";
import Shop from "./pages/Shop";
import Wheel from "./components/Wheel";
import Friends from "./pages/Friends";
import Tournament from "./pages/Tournament";
import League from "./pages/League";
import History from "./pages/History";
import Achievements from "./pages/Achievements";
import Admin from "./pages/Admin";
import MainMenu from "./components/MainMenu";
import Theme from "./components/Theme";
import BattlePass from "./pages/BattlePass";

function App(){

const [page,setPage]=useState("home");

return(

<div className="app">

<header>

<h1>
♠ CARD GAME
</h1>

<div>
🪙 25 000
💎 350
</div>

</header>

{
page==="home" &&
<main>

<div className="profile">

<img src="https://i.pravatar.cc/100"/>

<h2>
Игорь_user
</h2>

<p>
LVL 23
</p>

</div>

<div className="season">

<h2>
Сезон 1
</h2>

<p>
Путь чемпиона 🏆
</p>

</div>

<button 
className="play"
onClick={()=>setPage("game")}
>
  
БЫСТРАЯ ИГРА

</button>
  

<div className="buttons">

<button>
1 VS 1
</button>

<button>
4 игрока
</button>

<button>
6 игроков
</button>


</div>


</main>

}

{
page==="profile" &&
<div className="card">

<h2>
Профиль
</h2>

<p>
Игрок: Игорь_user
</p>

<p>
ELO: 1250
</p>

<p>
Winrate: 68%
</p>

</div>

}

{
page==="game" &&
<GameTable/>
}

{
page==="shop" &&
<Shop/>
}

{
page==="wheel" &&
<Wheel/>
}

{
page==="friends" &&
<Friends/>
}

{
page==="tournament" &&
<Tournament/>
}

{
page==="league" &&
<League/>
}

{
page==="history" &&
<History/>
}

{
page==="achievements" &&
<Achievements/>
}

{
page==="admin" &&
<Admin/>
}

{
page==="battlepass" &&
<BattlePass/>
}

{
page==="home" &&
<MainMenu 
setPage={setPage}
/>
}

<nav>

<button onClick={()=>setPage("home")}>
🏠
</button>

<button onClick={()=>setPage("profile")}>
👤
</button>

<button>
💬
</button>

<button>
⚙️
</button>

<button onClick={()=>setPage("shop")}>
🛒
</button>

<button onClick={()=>setPage("wheel")}>
🎡
</button>

<button 
onClick={()=>setPage("friends")}
>
👥
</button>

<button 
onClick={()=>setPage("tournament")}
>
🏆
</button>

<button 
onClick={()=>setPage("league")}
>
🏅
</button>

<button onClick={()=>setPage("history")}>
📜
</button>

<button onClick={()=>setPage("achievements")}>
🏅
</button>

<button onClick={()=>setPage("admin")}>
⚙️
</button>

<button
onClick={()=>setPage("battlepass")}
>
🎫
</button>

</nav>

<Theme/>

</div>

);
}

export default App;
