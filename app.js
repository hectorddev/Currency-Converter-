let { exec } = require('child_process')
const path = require('path')
const ruta = path.join(__dirname, '/Scraper/Scraper/spiders/run.py')


async function execScript() {
    await exec(ruta, function(err, stdout, stderr){
        if(err){
            console.log(err)
        }
        console.log(`stdout ${stdout}`)
        console.log(`stderr${stderr}`)
    })
}

execScript()