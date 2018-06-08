#!/usr/bin/env python
import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response
from firebase import firebase
import weather
import crolling_food_lib
import INUnoti_yj
from random import *
import INUnews

# Flask app should start in global layout
app = Flask(__name__)

firebase = firebase.FirebaseApplication('https://newssenger-69a99.firebaseio.com/')
firebase.post('/all/notification', {'name':'pushNotification','text': INUnoti_yj.mostView_title})
firebase.post('/all/chat', {'name':'pushNotification','text': INUnoti_yj.mostView_link + '@' + INUnoti_yj.mostView_title})


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    print("starting processRequest...", req.get("result").get("action"))
    if req.get("result").get("action") == "weather":
        speech = weather.nowWeather + weather.getDust() + "@null"
    elif req.get("result").get("action") == "menumenu":
        speech = crolling_food_lib.tmp + "@null"
    elif req.get("result").get("action") == "INUnoti":
        result = req.get("result")
        parameters = result.get("parameters")
        zone = parameters.get("noti_category")
        noti = INUnoti_yj.INUimFor()
        num = randint(0, len(noti[zone])-1)
        speech = noti[zone][num]
    elif req.get("result").get("action") == "liblib":
        speech = crolling_food_lib.libseat + "@null"
    elif req.get("result").get("action") == "newsnews":
        num = randint(0, len(INUnews.inunews) - 1)
        speech = INUnews.inunews[num]
    else: return{"webhook error"}

    print("Response:")
    print(speech)
    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        #"contextOut": [],
        "source": "Newssenger"
    }

@app.route('/static_reply', methods=['POST'])
def static_reply():
    speech = "Hello there, this reply is from the webhook !! "
    my_result =  {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }
    res = json.dumps(my_result, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

if __name__ == '__main__':
    port = int(os.getenv('PORT', 80))
    print ("Starting app on port %d" %(port))
    app.run(debug=False, port=port, host='0.0.0.0')

