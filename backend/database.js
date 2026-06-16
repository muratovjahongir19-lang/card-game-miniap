const users = [];


function createUser(player){

const user={

id:player.id,

name:player.name,

money:25000,

elo:1000,

wins:0,

losses:0,

friends:[]

};


users.push(user);

return user;

}



function getUser(id){

return users.find(
u=>u.id===id
);

}



module.exports={
users,
createUser,
getUser
};
