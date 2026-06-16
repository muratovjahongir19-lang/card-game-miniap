const mongoose=require("mongoose");


const UserSchema=new mongoose.Schema({

telegramId:{
type:String,
unique:true
},


name:String,


photo:String,


coins:{
type:Number,
default:25000
},


gems:{
type:Number,
default:350
},


elo:{
type:Number,
default:1000
},


wins:{
type:Number,
default:0
},


losses:{
type:Number,
default:0
},


vip:{
type:Boolean,
default:false
}


});


module.exports=
mongoose.model(
"User",
UserSchema
);
