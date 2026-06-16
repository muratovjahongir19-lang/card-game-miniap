import React,{useState,useEffect} from "react";
import socket from "../socket";


export default function TableChat(){


const [text,setText]=useState("");

const [messages,setMessages]=useState([]);



useEffect(()=>{


socket.on(
"tableChat",
(data)=>{

setMessages(
old=>[
...old,
data
]
);

}

);


},[]);



function send(){


socket.emit(
"tableChat",
text
);


setText("");

}



return(

<div className="chat-box">


<div>

{

messages.map((m,i)=>(

<p key={i}>

👤 {m}

</p>

))

}

</div>



<input

value={text}

onChange={
e=>setText(e.target.value)
}

/>


<button onClick={send}>

💬

</button>



</div>


)

}
