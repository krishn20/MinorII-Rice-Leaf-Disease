import React from 'react'

function Step(props) {
    return(
        <div className="step">
            <h1>{props.name}</h1>
            <img src={props.path}/>
        </div>
    )
}

export default Step