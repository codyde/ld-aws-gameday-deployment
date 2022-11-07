import json
from flask_cors import CORS
from flask import Flask,jsonify, request, render_template, session
from flask_session import Session 
import ldclient
from ldclient.config import Config
import os
import eventlet
import uuid
import boto3
eventlet.monkey_patch()
from config import ApplicationConfig


app = Flask(__name__, static_url_path='',
                  static_folder='out',
                  template_folder='out')
app.config.from_object(ApplicationConfig)

server_session = Session(app)

LD_KEY = os.environ.get('LD_SERVER_KEY')

status_api = 'v2.3344'

fallback = '{"dbhost": "db","dbname": "localdb","mode": "Local"}'

user = {
    "key": "anonymous"
}
ldclient.set_config(Config(LD_KEY))


@app.route('/')
def default_path():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def app_login():
    request_data = request.get_json()
    session['key'] = request_data['key']
    status = {
        "status": session['key']+" has been logged in"
    }
    return jsonify(status) 

@app.route("/logout")
def app_logout():
    session.pop('key', default=None)
    status = {
        "status":"logged out"
    }
    return jsonify(status)

@app.route("/status")
def get_status():
    ldclient.set_config(Config(LD_KEY))
    user = {
        "key": 'anonymous'
    }
    ldclient.get().identify(user)
    SiteStatus = ldclient.get().variation('siteRelease', user, False)
    print(SiteStatus)
    if SiteStatus == True: 
        data = {
            "app-version": status_api
        }
        return jsonify(data)
    else:
        data = {
            "data": "no-data"
        }
        return jsonify(data)


@app.route("/health")
def get_api():
    ldclient.set_config(Config(LD_KEY))
    try:
        user = {
            "key": session['key']
        }
    except:
        user = {
            "key": 'debuguser'
        }
    ldclient.get().identify(user)
    dbinfo = ldclient.get().variation('dbDetails', user, fallback)
    print(user)
    try:
        if dbinfo['mode'] == "Cloud":
            stats = {
                'version': '2',
                'status': 'Healthy - Migration Successful',
                'location': 'Cloud'
            }
            
        else:
            stats = {
                'version': '1',
                'status': 'unhealthy',
                'location': 'DebugData'
            }
        return jsonify(stats)
    except:
        stats = {
                'version': '1',
                'status': 'unhealthy',
                'location': 'DebugData'
            }
        return  jsonify(stats)

@app.route("/datas", methods=["GET", "POST"])
def thedata():
    ldclient.set_config(Config(LD_KEY))
    try:
        user = {
            "key": session['key']
        }
    except: 
        user = {
            "key": 'debuguser'
        }
    ldclient.get().identify(user)
    logstatus = ldclient.get().variation('logMode', user, 'default')

    ### DEV NOTES ###

    # JSON based feature flags allow us to push configuration blocks that we can parse and use within our application code. 
    
    # The code to use Feature Flags to migrate our data is below, as well as the parameters to create in Launchdarkly. When you create these in LaunchDarkly, it is recommended to copy and paste these values
    
    # Flag Name/Key - dbDetails
    # Flag Type - JSON
    # Variation 1 (On)  - {"dbhost": "dynamodb","gamedaydb": "localdb","mode": "Cloud"}
    # Variation 2 (Off) - {"dbhost": "db","dbname": "localdb","mode": "Local"}

    dbinfo = ldclient.get().variation('dbDetails', user, fallback)
    print(dbinfo)
    if dbinfo['dbhost'] == 'db':
        dummyData = [(
            {
                "id":1,
                "title":"DEBUG - Database TODO",
                "text":"I really hope we don't forget to create the flag to enable the new database connection"
            },
            {
                "id":2,
                "title":"DEBUG - Wow this design",
                "text":"So much CSS was used to get boxes to line up and I bet they are still uneven."
            },
            {
                "id":3,
                "title":"DEBUG - I need dinner",
                "text":"I've been coding for what seems like years and I still have no idea what im picking up for dinner."
            }
        )]
        return jsonify(dummyData)
    else:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('GamedayDB')
        data = table.get_item(Key={'teamid': 'GDTEAM'})
        realData = [(
            {
                "id":1,
                "title":data['Item']['title1'],
                "text":data['Item']['text1']
            },
            {
                "id":1,
                "title":data['Item']['title2'],
                "text":data['Item']['text2']
            },
            {
                "id":1,
                "title":data['Item']['title3'],
                "text":data['Item']['text3']
            }
        )]
        return jsonify(realData)

@app.route("/teamdebug")
def teamdebug():
    try:
        user = {
            "key": session['key']
        }
    except:
        user = {
            "key": "debuguser"
        }
    ldclient.get().identify(user)
    logstatus = ldclient.get().variation('logMode', user, 'default')
    ### DEV NOTES ###

    # We can hide components behind a feature flag, and use targeting rules to control which users can see them - like a debug menu for a database connection
    
    # Debug mode feature flag is below. Ensure it's been created in LaunchDarkly. This is a multi-variate string. This means you can create multiple version of this flag that return different results. 

    # Flag Name/Key - logMode
    # Flag Type - String
    # Variation 1 (On)  - 'debug'
    # Variation 2 (Off) - 'default' 
    if logstatus == "debug":
        teamid = "GDTEAM"
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('GamedayDB')
        data = table.get_item(Key={'teamid': str(teamid)})
        teamval = {
            "teamid": teamid,
            "loglevel": logstatus,
            "debugcode": data['Item']['debugcode']
        }
        return jsonify(teamval)
    else:
        data = {
            "loglevel": logstatus,
            "message": "Logging is currently in default mode. No debug data available. Have you checked LaunchDarkly?"
        }
        return jsonify(data)
   

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response