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

def getCrimes():
    crimes = db.query_db('select category, month, lat, lon from crimes')
    return crimes

# Handle requests to report
@app.route('/report', methods = ['GET', 'POST'])
def reportCrime():
    if request.method == 'GET':
        crimes = getCrimes()
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