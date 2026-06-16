import React,{useState} from "react";

import api from "../api";


export default function Login(){


const [user,setUser]=useState(null);



async function login(){


let res=
await api.post(
"/login",
{


telegramId:
"123456",


name:
"Player",


photo:
"avatar"


}

);


setUser(res.data.user);


}



return(

<div>


<button onClick={login}>

Войти через Telegram

</button>



{

user &&

<h2>
Привет {user.name}
</h2>

}



</div>

)

}
