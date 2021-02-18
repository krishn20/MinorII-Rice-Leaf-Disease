import time
from flask import Flask,request,jsonify

app = Flask(__name__)

"""@app.route('/time')
def get_current_time():
    return {'time': time.time()}
"""

@app.route('/evaluate',methods=["POST"])
def evaluate():
    image= request.get_json()
    print(image['file'])
    return 'done'

@app.route('/getResult',methods=["GET"])
def getResult():
    result=[]
    result.append({'backgroundRemoval':"path"})
    return jsonify({'results':result})
