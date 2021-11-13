const express = require('express')
const mongoose = require('mongoose')
const router = require('./routes/routes.js')
const cors = require('cors')


const app = express()
const port = 5500


const URL = "mongodb+srv://dbPractice:test123@cluster0.8zqnh.mongodb.net/Cluster0?retryWrites=true&w=majority"

mongoose.connect(URL, {
    useNewUrlParser: true,
    useUnifiedTopology: true
}).then(() => console.log('Conected'))


//Los middlewares son bloques de código que se ejecutan entre la petición del usuario y la respuesta del servidor
app.use(express.json({limit: "50mb"}))
app.use(express.urlencoded({extended: true}))
app.use(cors())

/* app.get('/', (req, res) =>{
    res.send('Hello!')
}) */

app.use(router)
app.use('/api/converter', router)



app.post('/api/converter', (req, res) => {
    console.log(req.body)
    res.send('You have posted something')
})




app.listen(port, () => {
    console.log(`Server is listening at http://localhost:${port}`)
})

