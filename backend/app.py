# Code imported from the flask documentation
# https://flask.palletsprojects.com/en/2.0.x/patterns/singlepageapplications/

import os

from flask import Flask, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(__name__)
app.config['FLASK_ENV']='development'

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# example page
@app.route("/heartbeat")
def heartbeat():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(debug=True)