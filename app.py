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
        str_data = data["message"]
        split_data = data["message"].split()
        print("str data")
        print(str_data)
        print("Split data")
        print(split_data)
        try:
            try:
                if ("!item" in split_data):
                    response = plain_palico_bot.items(split_data)

            except Exception as e:
                print(e)
                return(jsonify("Did you mean: !item honey low|high|g-rank...?"))

            try: 
                if ("!key" in split_data):
                    response = plain_palico_bot.keyquest(split_data)

            except Exception as e:
                print(e)
                return(jsonify("Did you mean: !key hub|village 1|2|3..?"))
                
            print(response)

        except Exception as e:
            print(e)
            print("Error!")
            if(plain_palico_bot.error != ""):
                return jsonify(plain_palico_bot.error)

        return jsonify(response)
    else:
        return "Error!"