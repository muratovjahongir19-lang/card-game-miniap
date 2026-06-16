import React,{useEffect,useState} from "react";


export default function Timer(){

const [time,setTime]=useState(15);



useEffect(()=>{


const t=setInterval(()=>{


setTime(
old=>old>0?old-1:15
);


},1000);



return()=>clearInterval(t);


},[]);



return(

<div className="timer">

Ваш ход: {time}

</div>

)

}
