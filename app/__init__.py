# Code imported from the flask documentation
# https://flask.palletsprojects.com/en/2.0.x/patterns/singlepageapplications/

import os

from flask import Flask, jsonify, render_template

app = Flask(__name__)

# example page
@app.route("/heartbeat")
def heartbeat():
    return jsonify({"status": "healthy"})


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    title="CrimeMapper"
    
    return render_template("index.html", title=title#, data=data)
    )