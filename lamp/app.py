from flask import Flask,request
import json
from json import JSONEncoder
from flask.helpers import stream_with_context
import requests
import uuid
import logging

logging.basicConfig(level=logging.DEBUG)


class lamp:
    def __init__(self,switch_State,dimmer_State):
        
        self.id=int(uuid.uuid4())
        self.switch_State=switch_State
        self.dimmer_State=dimmer_State
        
        logging.debug ("New Lamp generated")
        logging.debug (f'UUID: {self.id}')
        logging.debug (f'Switchstate: {self.switch_State}')
        logging.debug (f'Dimmer State: {self.dimmer_State}')

 
class ClassEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__

    
lamp1=lamp('Off',0)

app = Flask(__name__)


def check_Dimmer_Value(dimmer_Value):
    value_To_Check=int(dimmer_Value)
    if 0<=value_To_Check<=100:
        logging.debug(f"Value of Dimmer Valid. Value: {value_To_Check}")
        return True
    else:
        logging.debug(f"invalid Value")
        return False
    return

def set_Dimmer_Value(dimmer_Value):
    lamp1.dimmer_State=dimmer_Value
    return

@app.route('/', methods=['POST','GET','PUT'])
def index():
    if request.method=='GET':
        return ((ClassEncoder().encode(lamp1)))
    
    if request.method=='POST':
        return 'Method not yet implemented'        

    if request.method=='PUT':
        data=json.loads(request.data)
        logging.debug(data)
        
        if (data['switch_State']=='On'):
            logging.debug(data['switch_State'])
            lamp1.switch_State=data['switch_State']
            
            if (data['dimmer_State']):
                if (check_Dimmer_Value(data['dimmer_State'])):
                    set_Dimmer_Value((data['dimmer_State']))
          

        if (data['switch_State']=='Off'):
            logging.debug(data['switch_State'])
            lamp1.switch_State=data['switch_State']

            if (data['dimmer_State']):
                if (check_Dimmer_Value(data['dimmer_State'])):
                    set_Dimmer_Value((data['dimmer_State']))
           

       
        return (ClassEncoder().encode(lamp1))

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, use_reloader=True,port=5001)