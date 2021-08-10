let { exec } = require('child_process')
const path = require('path')
const ruta = path.join(__dirname, './Scraper/Scraper/spiders/run.py')


exec(ruta, function(err){
    if(err){
        console.log(err)
    }
})