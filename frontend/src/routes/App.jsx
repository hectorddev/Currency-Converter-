import React from 'react'
import {BrowserRouter, Route, Switch} from 'react-router-dom'

import Layout from '../components/Layout.jsx'
import Home from '../containers/Home.jsx'
import Converter from '../containers/Converter.jsx'


const App = () => {
    return (
        <BrowserRouter>
            <Layout>
                <Switch>
                    <Route exact path="/" component={Home}></Route>
                    <Route exact path="/converter/:money/:value1/:value2" component={Converter}></Route>

                </Switch>
            </Layout>
        </BrowserRouter>    
    )
}

export default App
