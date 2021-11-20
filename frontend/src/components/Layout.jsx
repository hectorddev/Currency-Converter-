import React from 'react'

import Header from '../components/Header.jsx'
import Footer from '../components/Footer.jsx'

import '../styles/Layout.css'

const Layout = ({children}) => {
    return (
        <div className="Main">
            <Header />
            {children}
            <Footer />
        </div>
    )
}

export default Layout
