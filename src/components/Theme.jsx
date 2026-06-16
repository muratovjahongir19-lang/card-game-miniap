import React,{useState} from "react";


export default function Theme(){


const [dark,setDark]=useState(true);



function change(){

setDark(!dark);

document.body.className=
dark?"light":"dark";

}



return(

<button onClick={change}>

🎨 Тема

</button>

)

}
