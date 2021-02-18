import React,{useState} from 'react'
import {Link} from 'react-router-dom'

function LandingPage(props){
    const [file, setfile] = useState('')

    function handleClick(event){
        const response= fetch('/evaluate',{
            method: 'POST',
            headers:{
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({file})
        })
        if(response.ok){
            console.log("great")
        }
        }
    
    function handleChange(event){
        setfile(event.target.value)
    }

return(
    <div className="landingPage">
       <h1> Rice Leaf Disease Detection </h1>
       <div className="landingPage__flex">
            <div className="landingPage__disease">
            <h2> Rice Leaf Top 3 Diseases are: </h2>
            <ul>
                <li>Bacterial leaf blight</li>
                <li>Brown spot</li>
                <li>Leaf smut</li>
            </ul>
            </div>
            <div className="landingPage__test">
                <h2> Test your leaf here! </h2>
                <form>
                    <input type="file" id="inputImage" name="inputImage" value={file} onChange={handleChange} />
                   <Link to="/evaluate"> <button onClick={handleClick}> Start Testing </button> </Link> 
                </form>
                    
            </div>
       </div>
    </div>
)
}

export default LandingPage