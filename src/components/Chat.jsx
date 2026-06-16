import React,{useState,useEffect} from "react";

import socket from "../socket";


export default function Chat(){


const [msg,setMsg]=useState("");

const [chat,setChat]=useState([]);



useEffect(()=>{


socket.on(
"chat",
(data)=>{


setChat(
old=>[
...old,
data
]
);


});


},[]);



function send(){


socket.emit(
"message",
msg
);


setMsg("");

}



return(

<div>


<div className="chat">


{
chat.map((m,i)=>(

<p key={i}>

<b>{m.name}</b>:
{m.text}

</p>


))

}


</div>



<input

value={msg}

onChange={
e=>setMsg(e.target.value)
}

/>


<button onClick={send}>

Отправить

</button>



</div>


)

}
