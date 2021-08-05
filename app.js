let { PythonShell } = require('python-shell')
const path = require('path')
const ruta = path.join(__dirname, './Scraper/Scraper/spiders/run.py')


PythonShell.run(ruta, null, (err) => {
    if(err) throw(err)
    console.log('Finished')
}) 