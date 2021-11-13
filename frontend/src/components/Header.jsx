import React from 'react'
import '../styles/Header.css'

const Header = () => {
    return (
        <div className="Header">
            <nav className="navbar navbar-light bg-light">
                <div className="container">
                    <a className="navbar-brand" href="#">
                        Logo
                    </a>
                </div>
            </nav>
        </div> 
    )
}

export default Header
