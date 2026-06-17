const express = require("express");

const router = express.Router();

const BattlePass =
require("../models/BattlePass");


router.get("/:userId", async(req,res)=>{

const pass =
await BattlePass.findOne({

userId:req.params.userId

});

res.json(pass);

});


router.post("/xp", async(req,res)=>{

const {userId,xp}=req.body;

let pass =
await BattlePass.findOne({userId});

if(!pass){

pass = await BattlePass.create({
userId
});

}

pass.xp += xp;

while(pass.xp >= 100){

pass.level++;
pass.xp -= 100;

}

await pass.save();

res.json(pass);

});

module.exports = router;
