from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/encode", methods=["POST"])
def encode():
    data = request.json
    text = data.get("text", "")
    dictionary = data.get("dictionary", {})

    for word, code in dictionary.items():
        text = text.replace(word, code)

    return jsonify({"result": text})


@app.route("/decode", methods=["POST"])
def decode():
    data = request.json
    text = data.get("text", "")
    dictionary = data.get("dictionary", {})

    reverse_dict = {v: k for k, v in dictionary.items()}

    for code, word in reverse_dict.items():
        text = text.replace(code, word)

    return jsonify({"result": text})


@app.route("/")
def home():
    return "NLP Server is running!"
