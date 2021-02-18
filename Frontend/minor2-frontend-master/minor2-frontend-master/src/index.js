import React from 'react'
import ReactDom from 'react-dom'
import App from './components/App'
import "./styles/style.css"
import {BrowserRouter as Router} from 'react-router-dom'

ReactDom.render(
    <Router>
        <App />
    </Router>
    ,document.getElementById("root")
)