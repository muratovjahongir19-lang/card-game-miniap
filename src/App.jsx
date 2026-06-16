import GameTable from "./pages/GameTable";
import Shop from "./pages/Shop";
import Wheel from "./components/Wheel";
import Friends from "./pages/Friends";
import Tournament from "./pages/Tournament";
import League from "./pages/League";

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

{
page==="shop" &&
<Shop/>
}


{
page==="wheel" &&
<Wheel/>
}

<button onClick={()=>setPage("shop")}>

🛒

</button>


<button onClick={()=>setPage("wheel")}>

🎡

</button>

</nav>



</div>

)
  
{
page==="game" &&
<GameTable/>
}
  
}


export default App;
