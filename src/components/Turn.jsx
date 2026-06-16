import React,{useEffect,useState} from "react";


export default function Turn(){


const [time,setTime]=useState(15);



useEffect(()=>{


let t=setInterval(()=>{


setTime(
x=>x>0?x-1:15
);


},1000);



return()=>clearInterval(t);


},[]);



return(

<div className="timer">

⏳ {time}

</div>

)

}
