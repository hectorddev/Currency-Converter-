import React from 'react'
import ReactDOM from 'react-dom'
import App from './routes/App.jsx'

ReactDOM.render(<App />, document.getElementById('app'))



/* let { exec } = require('child_process')
const path = require('path')
const ruta = path.join(__dirname, '../Scraper/Scraper/spiders/scraper.py')


async function execScript() {
    await exec(ruta, function(err, stdout, stderr){
        if(err){
            console.log(err)
        }
        console.log(`stdout ${stdout}`)
        console.log(`stderr${stderr}`)
    })
}

execScript() */