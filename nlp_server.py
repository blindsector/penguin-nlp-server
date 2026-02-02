import spacy
from flask import Flask, request, jsonify
from flask_cors import CORS

# Зареждаме български модел
nlp = spacy.load("bg_core_news_sm")

app = Flask(__name__)

# 🔥 РАЗРЕШАВАМЕ ВСИЧКИ ВРЪЗКИ ОТ ВЪНШНИ САЙТОВЕ
CORS(app, resources={r"/*": {"origins": "*"}})


def preserve_case(original, new):
    if original.isupper():
        return new.upper()
    if original[0].isupper():
        return new.capitalize()
    return new


def transform_text(text, dictionary, reverse=False):
    doc = nlp(text)
    result = []

    for token in doc:
        word = token.text
        key = word.lower()

        if reverse:
            reverse_dict = {v.lower(): k for k, v in dictionary.items()}
            if key in reverse_dict:
                new_word = preserve_case(word, reverse_dict[key])
                result.append(new_word)
            else:
                result.append(word)
        else:
            if key in dictionary:
                new_word = preserve_case(word, dictionary[key])
                result.append(new_word)
            else:
                result.append(word)

    return " ".join(result)


@app.route("/")
def home():
    return "NLP Server is running!"


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
