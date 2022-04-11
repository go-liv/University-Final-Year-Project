from flask import Flask, jsonify, request
from flask_cors import CORS

import db

app = Flask(__name__)
app.config.from_object(__name__)
app.config['FLASK_ENV']='development'
app.config['DATABASE'] = './db/crime.db'

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
    if (zoom <= 16.0 or zoom >= 15.0):
        latdiff = 0.0035
        londiff = 0.0165

    crimes = db.query_db('select category, month, lat, lon from crimes where lat between ' + str(lat - latdiff) + ' and ' + str(lat + latdiff) 
     + ' and lon between ' + str(lon - londiff) + ' and ' + str(lon + londiff))
    return crimes

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
        return jsonify({'status': 'crime reported'})
        

if __name__ == '__main__':
    app.run(debug=True)