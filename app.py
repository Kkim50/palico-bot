from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import plain_palico_bot

app = Flask(__name__)

@app.route('/api/', methods=['GET', 'POST'])
@cross_origin()
def api_post():
    if (request.method == 'POST'):
        data = request.get_json()
        print data["message"]
        print data["user"]

        return jsonify(plain_palico_bot.response)
    else:
        return "Error!"