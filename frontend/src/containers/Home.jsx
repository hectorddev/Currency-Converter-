import React, {Fragment, useState} from 'react'
import { Link } from 'react-router-dom'
import CurrencyInput from 'react-currency-input-field'
import '../styles/bootstrap.min.css'


const Home = () => {

    const [money, setMoney] = useState({
        currency: '0',
        value1: 'bs',
        value2:'cop'
    })

    const handleInputChange = (event) => {
        console.log(event.target.value)
        setMoney({
            ...money,
            [event.target.name] : event.target.value 
        })
        console.log(money)
    }


    const enviarDatos = (event) => {
        event.preventDefault()
    }


    return (
        <Fragment>
            <form className="row g-3" onSubmit={enviarDatos}>
                <div className="col-lg-12">
                    <label htmlFor="currency">Convertir</label>
                    <CurrencyInput
                        id="currency"
                        name="currency"
                        placeholder="Please, enter a number"
                        disableGroupSeparators={true}
                        onChange={handleInputChange}
                       
                    >

                    </CurrencyInput>

                    <select name="value1" id="value1" onChange={handleInputChange}>
                        <option value="bs" defaultValue>BS</option>
                        <option value="cop">COP</option>
                        <option value="usd">USD</option>
                        <option value="btc">BTC</option>
                    </select>
                    <select name="value2" id="value2" onChange={handleInputChange}>
                        <option value="cop" defaultValue>COP</option>
                        <option value="bs">BS</option>
                        <option value="usd">USD</option>
                        <option value="btc">BTC</option>
                    </select>
                    <Link to={`/converter/${money.currency}/${money.value1}/${money.value2}`}>
                    <button type="submit">Convertir</button>
                    </Link>
                </div>
            </form>
        </Fragment>
    )
}

export default Home
