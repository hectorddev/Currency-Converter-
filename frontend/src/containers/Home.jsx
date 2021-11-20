import React, {Fragment, useState} from 'react'
import { Link } from 'react-router-dom'
import CurrencyInput from 'react-currency-input-field'
import '../styles/Home.css'


const Home = () => {

    const [money, setMoney] = useState({
        currency: '0',
        value1: 'bs',
        value2:'cop'
    })

    const handleInputChange = (event) => {
        setMoney({
            ...money,
            [event.target.name] : event.target.value 
        })
    }


    const enviarDatos = (event) => {
        event.preventDefault()
    }


    return (
        <Fragment>
            <form className="form" onSubmit={enviarDatos}>
                <div className="form_container">
                    <div className="form_container--idea">
                        <h2>
                            Welcome to conVErter
                        </h2>
                        <h5>
                        You can change the following currencies

                        </h5>
                        <div className="container--idea">
                            <ul>
                                <li className="currencies">BS: Bolívar</li>
                                <li className="currencies">USD: Dollar</li>
                                <li className="currencies">COP: Colombian Peso</li>
                                <li className="currencies">BTC: Bitcoin</li>                            </ul>
                        </div>
                    </div>
                    <div className="form_container--inputs">
                        <div className="container--inputs">
                            <CurrencyInput
                                id="currency"
                                className="input_currency"
                                name="currency"
                                placeholder="I want converter..."
                                disableGroupSeparators={true}
                                onChange={handleInputChange}                       
                            >
                            </CurrencyInput>

                            <select className="input input_value1" name="value1" id="value1" onChange={handleInputChange}>
                                <option value="bs" defaultValue>BS</option>
                                <option value="cop">COP</option>
                                <option value="usd">USD</option>
                                <option value="btc">BTC</option>
                            </select>
                        </div>
                        <div className="container--toConverter">
                            <p className="paragraph">To</p>
                            <select className="input input_value2" name="value2" id="value2" onChange={handleInputChange}>
                                <option value="cop" defaultValue>COP</option>
                                <option value="bs">BS</option>
                                <option value="usd">USD</option>
                                <option value="btc">BTC</option>
                            </select>
                        </div>
                    </div>
                    <Link to={`/converter/${money.currency}/${money.value1}/${money.value2}`}>
                    <button className="button_submit" type="submit">Turn It</button>
                    </Link>
                </div>
            </form>
        </Fragment>
    )
}

export default Home
