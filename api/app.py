from pyparsing import dblSlashComment
from flask import Flask, jsonify, request
from flask_cors import CORS

import json
import db

app = Flask(__name__)
app.config.from_object(__name__)
app.config['FLASK_ENV']='development'
app.config['DATABASE'] = './db/crime.sqlite'

# Enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# Init db functions
db.init_app(app)

def getCrimes(lat, lon, zoom):
    if(zoom <= 12.0 or zoom >= 11.0):
        latdiff = 0.02765
        londiff = 0.13175
    if (zoom <= 14.0 or zoom >= 13.0):
        latdiff = 0.00705
        londiff = 0.03285
    if (zoom >= 15.0):
        latdiff = 0.0035
        londiff = 0.0165

    crimes = db.query_db("SELECT * FROM crimes WHERE lat BETWEEN ? AND ? AND lon BETWEEN ? AND ?", (float(lat - latdiff), float(lat + latdiff), float(lon - londiff), float(lon + londiff)))
    print(crimes)
    return crimes

def insertCrime(lat, lon, month, category):
    print("INSERT INTO crimes (category, month, lat, lon) VALUES (?, ?, ?, ?)", (str(category), str(month), float(lat), float(lon)))
    dbCopy = db.get_db()
    dbCopy.execute("INSERT INTO crimes (category, month, lat, lon) VALUES (?, ?, ?, ?)", (str(category), str(month), float(lat), float(lon)))
    dbCopy.commit()

# Handle requests to report
@app.route('/report', methods = ['GET', 'POST'])
def reportCrime():
    if request.method == 'GET':
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        zoom = request.args.get('zoom')
        crimes = getCrimes(float(lat), float(lon), float(zoom))
        result = []
        for i, crime in enumerate(crimes):
            print(crime)
            each = {
                'type': 'Feature',
                'properties': {
                    'type': 'user (use at your own discretion)',
                    'category': crime['category'],
                    'month': crime['month'],
                },
                'geometry': {
                    'type': 'Point',
                    'coordinates': [crime['lon'], crime['lat']],
                },
            }
            result.insert(i, each)
        
        return jsonify({'body': result})

    if request.method == 'POST':
        if (request.headers.get('Content-Type') == 'application/json'):
            body = request.json
            month = body['date']['monthIndex']
            if month < 10:month = '0' + str(month)
            year = body['date']['year']
            date = str(year) + '-' + str(month)
            insertCrime(body['coordinates'][1], body['coordinates'][0], date, body['category'])
            return jsonify({
                'body': {
                    'coordinates': body['coordinates'],
                    'date': body['date'],
                    'category': body['category']
                }
            })
        else:
            return 'Content type must be application/json', 415
        

if __name__ == '__main__':
    app.run(debug=True)