from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def preserve_case(original, new):
    if original.isupper():
        return new.upper()
    if original[0].isupper():
        return new.capitalize()
    return new

def smart_replace(word, dictionary, reverse=False):
    endings = ["ите", "ът", "та", "то", "а", "я", "и"]

    base_word = word.lower()

    for ending in endings:
        if base_word.endswith(ending):
            root = base_word[:-len(ending)]
            break
    else:
        root = base_word
        ending = ""

    if reverse:
        reverse_dict = {v: k for k, v in dictionary.items()}
        if root in reverse_dict:
            new_root = reverse_dict[root]
        else:
            return word
    else:
        if root in dictionary:
            new_root = dictionary[root]
        else:
            return word

    new_word = new_root + ending
    return preserve_case(word, new_word)

def transform_text(text, dictionary, reverse=False):
    words = text.split()
    result = [smart_replace(w, dictionary, reverse) for w in words]
    return " ".join(result)

@app.route("/")
def home():
    return "Penguin NLP Server Running 🐧"

@app.route("/encode", methods=["POST"])
def encode():
    data = request.json
    text = data.get("text", "")
    dictionary = data.get("dictionary", {})
    return jsonify({"result": transform_text(text, dictionary)})

@app.route("/decode", methods=["POST"])
def decode():
    data = request.json
    text = data.get("text", "")
    dictionary = data.get("dictionary", {})
    return jsonify({"result": transform_text(text, dictionary, reverse=True)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
