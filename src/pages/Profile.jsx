import React,{useEffect,useState} from "react";

import socket from "../socket";


export default function Profile(){


const [user,setUser]=useState(null);



useEffect(()=>{


socket.emit("profile");


socket.on(
"profileData",
(data)=>{

setUser(data);

}

);


},[]);



if(!user)

return <h2>Загрузка...</h2>



return(

<div className="card">


<h1>
👤 {user.name}
</h1>


<h2>
🪙 {user.money}
</h2>


<p>
🏆 ELO: {user.elo}
</p>


<p>
Победы: {user.wins}
</p>


<p>
Поражения: {user.losses}
</p>



</div>


)

}
