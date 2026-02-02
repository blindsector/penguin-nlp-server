import spacy
from flask import Flask, request, jsonify
from flask_cors import CORS

nlp = spacy.load("bg_core_news_sm")

app = Flask(__name__)

# 🔥 Това е ВАЖНАТА част
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

def preserve_case(original, new):
    if original.isupper():
        return new.upper()
    if original[0].isupper():
        return new.capitalize()
    return new


@app.route("/")
def home():
    return "Penguin NLP server is running!"


@app.route("/encode", methods=["POST", "OPTIONS"])
def encode():
    data = request.json
    text = data.get("text", "")
    dictionary = data.get("dictionary", {})

    words = text.split()
    encoded_words = [dictionary.get(word.lower(), word) for word in words]

    return jsonify({"result": " ".join(encoded_words)})


@app.route("/decode", methods=["POST", "OPTIONS"])
def decode():
    data = request.json
    text = data.get("text", "")
    dictionary = data.get("dictionary", {})

    reverse_dict = {v: k for k, v in dictionary.items()}
    words = text.split()
    decoded_words = [reverse_dict.get(word.lower(), word) for word in words]

    return jsonify({"result": " ".join(decoded_words)})


if __name__ == "__main__":
    app.run()
