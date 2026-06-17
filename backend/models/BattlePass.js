const mongoose = require("mongoose");

const BattlePassSchema = new mongoose.Schema({

userId:{
type:String,
required:true
},

level:{
type:Number,
default:1
},

xp:{
type:Number,
default:0
},

premium:{
type:Boolean,
default:false
}

});

module.exports = mongoose.model(
"BattlePass",
BattlePassSchema
);
