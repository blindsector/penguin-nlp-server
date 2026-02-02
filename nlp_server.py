import spacy
from flask import Flask, request, jsonify
from flask_cors import CORS

# Зареждаме българския модел
nlp = spacy.load("bg_core_news_sm")

app = Flask(__name__)
CORS(app)  # 👈 Това разрешава връзката от твоя сайт

def preserve_case(original, new):
    if original.isupper():
        return new.upper()
    if original[0].isupper():
        return new.capitalize()
    return new

def transform(text, dictionary, mode="encode"):
    doc = nlp(text)
    result = []

    # правим обърнат речник за декодиране
    reverse_dictionary = {v: k for k, v in dictionary.items()}

    for token in doc:
        if token.is_alpha:
            lemma = token.lemma_.lower()

            if mode == "encode" and lemma in dictionary:
                new_lemma = dictionary[lemma]
            elif mode == "decode" and lemma in reverse_dictionary:
                new_lemma = reverse_dictionary[lemma]
            else:
                result.append(token.text)
                continue

            new_word = preserve_case(token.text, new_lemma)
            result.append(new_word)
        else:
            result.append(token.text)

    return " ".join(result)

@app.route("/encode", methods=["POST"])
def encode_text():
    data = request.json
    text = data.get("text", "")
    dictionary = data.get("dictionary", {})
    return jsonify({"result": transform(text, dictionary, "encode")})

@app.route("/decode", methods=["POST"])
def decode_text():
    data = request.json
    text = data.get("text", "")
    dictionary = data.get("dictionary", {})
    return jsonify({"result": transform(text, dictionary, "decode")})

@app.route("/")
def home():
    return "Penguin NLP server is running!"
