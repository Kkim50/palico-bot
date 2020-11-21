from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import palico_bot.py

app = Flask(__name__)

@app.route('/api/', methods=['GET', 'POST'])
@cross_origin()
def api_post():
    if (request.method == 'POST'):
        return majorsfair.jsonfiles
    else:
        return "Hello World!"