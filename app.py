from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import plain_palico_bot

app = Flask(__name__)

@app.route('/api/', methods=['GET', 'POST'])
@cross_origin()
def api_post():
    response = ""

    if (request.method == 'POST'):
        data = request.get_json()
        print (data["message"])

        try:
            if ("!item" in data):
                response = plain_palico_bot.items(data)
            
            if ("!key" in data):
                response = plain_palico_bot.items(data)

            print(response)
            
        except Exception as e:
            print(e)
            print("Error: Command  not supported!")

        return jsonify(response)
    else:
        return "Error!"