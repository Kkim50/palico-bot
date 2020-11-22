from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import plain_palico_bot

app = Flask(__name__)

@app.route('/api/', methods=['GET', 'POST'])
@cross_origin()
def api_post():
    response = "Invalid input. Please try again!"

    if (request.method == 'POST'):
        data = request.get_json()
        split_data = data["message"]).split()

        try:

            if ("!item" in split_data):
                response = plain_palico_bot.items(split_data)
            
            if ("!key" in split_data):
                response = plain_palico_bot.keyquest(split_data)

            print(response)
            
        except Exception as e:
            print(e)
            print("Error: Command  not supported!")

        return jsonify(response)
    else:
        return "Error!"