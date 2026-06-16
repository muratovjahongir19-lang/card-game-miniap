const banned=[];



function checkPlayer(player){


if(player.money>1000000){


banned.push(player.id);


return false;

}


return true;


}



module.exports={
checkPlayer,
banned
}
