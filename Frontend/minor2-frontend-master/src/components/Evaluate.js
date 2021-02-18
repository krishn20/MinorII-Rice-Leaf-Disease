import React,{useEffect,useState} from 'react'
import Step from './Step'
import LeftProcess from './LeftProcess'

import originalImage from '../assets/originalImage.jpg'
import backgroundRemovedImage from '../assets/backgroundRemovedImage.jpg'
import diseaseSegmented from '../assets/diseaseSegmented.jpg'
import greenRegion from '../assets/greenRegion.jpg'
import greyImage from '../assets/greyImage.jpg'
import hsv from '../assets/hsv.jpg'
import lab from '../assets/lab.jpg'

function Evaluate(){

    const [responses, setresponse] = useState("Calculating...")

    useEffect(() => {
        fetch("/getResult",{
            headers : { 
              'Content-Type': 'application/json',
              'Accept': 'application/json'
             }
      
          }).then(response => 
            response.json().then(data => {
                if(data != null){
                    setresponse(data['result'])
                    console.log(data)
                }
            })
            )
    }, [])
    
    let result
    if(responses==1)
        result= "Bacterial leaf blight"
    else if(responses==2)
        result="Brown spot"
    else if(responses==3)
        result= "Leaf smut"
    else
        result="Calculating..."
   
    return(
        <div className="evaluateContainer">
            <LeftProcess />
            <div className="right">
            <div className="result">
                <h1>
                    Result: {result}
                </h1>
            </div>
            <h1 className="processHeading"> The Process: </h1>
                 <Step name="Original Image" path={originalImage} />
                 <Step name="Background Removed Image" path={backgroundRemovedImage} />
                 <Step name="Disease Segmented Image" path={diseaseSegmented} />
                 <Step name="Green Region Removed Image" path={greenRegion} />
                 <Step name="Grey Image" path={greyImage} />
                 <Step name="HSV Image" path={hsv} />
                 <Step name="LAB Image" path={lab} />
            </div>
        </div>
    )
    
}

export default Evaluate