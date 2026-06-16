import React,{useState} from "react";


export default function Friends(){


const [friends,setFriends]=useState([]);



function invite(){


setFriends([

...friends,

"Новый игрок"

]);


alert(
"Друг приглашён +1000 🪙"
);


}



return(

<div className="card">


<h1>
👥 Друзья
</h1>


<button onClick={invite}>

➕ Пригласить друга

</button>



<h3>

Ваши друзья:

</h3>



{

friends.map((f,i)=>(

<p key={i}>

👤 {f}

</p>


))

}



</div>


)

}
