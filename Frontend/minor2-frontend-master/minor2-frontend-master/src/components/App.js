import React from 'react'
import LandingPage from './LandingPage'
import Evaluate from './Evaluate'
import {Switch,Route} from 'react-router-dom'

function App(){
    return(
        <div>
            <Switch>
                <Route exact path="/"><LandingPage /></Route>
                <Route path="/evaluate"> <Evaluate /> </Route>
            </Switch>
        </div>
    )
}

export default App