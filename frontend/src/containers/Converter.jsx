import React, {useEffect, useState} from 'react'
import { useParams } from 'react-router'
import { Link } from 'react-router-dom'
import axios from 'axios'
import convertidor from '../components/convertidor.js'

const Converter = () => {
    const {money, value1, value2} = useParams()
    const objBase = {
        currency: money, 
        value1, 
        value2
    }
    const newMoney = Number(money)
    const [result, setResult] = useState(newMoney)


    useEffect(() => {
        async function Conection(){
            try {
                return await axios.get('http://localhost:5500')
            } catch (error) {
                console.log(error)
            }
        }
        new Conection()
        .then(response => {
            const objConverter = response.data[0]
            const convertion = convertidor(objBase, objConverter)
            setResult(convertion)
        })
    })

    return (
        <div>
            <h1>{result}</h1>
            
            <Link to="/">            
            <button type="button">Volver</button>
            </Link>
        </div>
       
            
       
    )
}

export default Converter
