const express = require('express')
const router = express.Router()
const doc = require('../../export/json_files/mean_currencies.json')



router.get('/', (req, res) =>{
    res.json(doc)
})


router.get('api/converter', (req, res) => {
    res.json(doc)
})

module.exports = router