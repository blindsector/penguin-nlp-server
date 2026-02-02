from flask import Flask, request, jsonify
from flask_cors import CORS
import stanza

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Изтегляне на модела (става само първия път)
stanza.download("bg")
nlp = stanza.Pipeline("bg", processors="tokenize,pos,lemma")

def preserve_case(original, new):
    if original.isupper():
        return new.upper()
    if original[0].isupper():
        return new.capitalize()
    return new

def inflect_bg(original_word, new_lemma, feats):
    """
    Опростено огъване според граматичните тагове
    feats пример: Gender=Neut|Number=Sing|Definite=Def
    """
    if not feats:
        return new_lemma

    # Определителен член
    if "Definite=Def" in feats:
        if "Gender=Fem" in feats:
            return new_lemma + "та"
        elif "Gender=Neut" in feats:
            return new_lemma + "то"
        elif "Gender=Masc" in feats:
            return new_lemma + "ът"

    # Множествено число
    if "Number=Plur" in feats:
        if new_lemma.endswith("а") or new_lemma.endswith("я"):
            return new_lemma[:-1] + "и"
        return new_lemma + "и"

    return new_lemma

def transform_text(text, dictionary, reverse=False):
    doc = nlp(text)
    reverse_dict = {v: k for k, v in dictionary.items()}
    output_words = []

    for sentence in doc.sentences:
        for word in sentence.words:
            original = word.text
            lemma = word.lemma.lower()
            feats = word.feats  # граматични тагове

            if reverse:
                replacement = reverse_dict.get(lemma)
            else:
                replacement = dictionary.get(lemma)

            if replacement:
                new_word = inflect_bg(original.lower(), replacement, feats)
                new_word = preserve_case(original, new_word)
                output_words.append(new_word)
            else:
                output_words.append(original)

    return " ".join(output_words)

@app.route("/encode", methods=["POST"])
def encode():
    data = request.json
    return jsonify({
        "result": transform_text(data.get("text", ""), data.get("dictionary", {}))
    })

@app.route("/decode", methods=["POST"])
def decode():
    data = request.json
    return jsonify({
        "result": transform_text(data.get("text", ""), data.get("dictionary", {}), reverse=True)
    })

@app.route("/")
def home():
    return "Penguin NLP Morph Server 🐧"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
