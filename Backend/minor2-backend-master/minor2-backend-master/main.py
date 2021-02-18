from minor2 import *
 
import time
from flask import Flask,request,jsonify

app = Flask(__name__)

"""@app.route('/time')
def get_current_time():
    return {'time': time.time()}
"""
imageName=''

@app.route('/evaluate',methods=["POST"])
def evaluate():
    image= request.get_json()
    print(image['file'])
    global imageName
    imageName= image['file'][12:]
    print(imageName)
    return 'done'

@app.route('/getResult',methods=["GET"])
def getResult():
    imagePath= './data/' + imageName
    print(imagePath)
    bgr_img= cv2.imread(imagePath)
    #print(bgr_img)
    y_pred= background_removal(bgr_img)
    print(y_pred[0])
    r= int(y_pred[0])
    print(r)
    result={"result":r}

    return result
