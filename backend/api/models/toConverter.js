const mongoose = require('mongoose')


const convertionSchema = mongoose.Schema({
    mean_usd_cop: Number,
    mean_usd_btc: Number,
    mean_usd_ves: Number
})
module.exports =  mongoose.model(toConverter, convertionSchema)