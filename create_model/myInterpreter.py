from flask import Flask, request, jsonify
from transformers import pipeline, BertTokenizer, BertForSequenceClassification
import re, torch, pickle

app = Flask(__name__)

# =============================================
# BERT + REGEX UNTUK ENTITY RECOGNITION
# =============================================

ner_pipeline = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")

def hybrid_entity_recognition(text):
    # --- 1. BERT-based entities ---
    bert_entities = ner_pipeline(text)
    standardized_bert_entities = [
        {
            "entity": ent["entity_group"],
            "word": ent["word"],
            "score": ent["score"],
            "start": ent["start"],
            "end": ent["end"],
        }
        for ent in bert_entities
    ]

    # --- 2. Regex patterns untuk entitas lokal kampus ---
    regex_patterns = {
        "EMAIL": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "DATE": r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
        "JENJANG": r"\b(Magister|Doktor|S2|S3)\b",
        "PRODI": r"\b(Teknik|Informatika|Manajemen Teknologi|Sipil|Industri|Fisika|Kimia|Statistika|Lingkungan|Arsitektur)\b",
        "FAKULTAS": r"\b(SCIENTICS|INDSYS|CIVPLAN|MARTECH|ELECTICS|SIMT|CREABIZ)\b",
        "PROGRAM": r"\b(PJJ|Reguler|Kerjasama|Profesional|Eksekutif|Hybrid)\b",
    }

    regex_entities = []
    for label, pattern in regex_patterns.items():
        for match in re.finditer(pattern, text, re.IGNORECASE):
            regex_entities.append({
                "entity": label.upper(),
                "word": match.group(),
                "score": 1.0,
                "start": match.start(),
                "end": match.end(),
            })

    # --- 3. Gabungkan semua entity ---
    all_entities = standardized_bert_entities + regex_entities
    return all_entities


# =============================================
# INTENT CLASSIFICATION MODEL
# =============================================

def load_intent_model(model_path="my_intent_model_pasca"):
    """Load BERT intent model dan label encoder"""
    model = BertForSequenceClassification.from_pretrained(model_path)
    tokenizer = BertTokenizer.from_pretrained(model_path)
    with open(f"{model_path}/label_encoder.pkl", "rb") as f:
        label_encoder = pickle.load(f)
    model.eval()
    return model, tokenizer, label_encoder

model, tokenizer, label_encoder = load_intent_model("my_intent_model_pasca")

def replace_entity(text, entity_value, placeholder):
    pattern = re.escape(entity_value)
    return re.sub(pattern, placeholder, text)

def get_intent(text, model, tokenizer, label_encoder, entity_list, modtext):
    """Prediksi intent dari teks (dengan placeholder)"""
    inputs = tokenizer(modtext, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        pred_idx = torch.argmax(probs, dim=1).item()
        intent_name = label_encoder.inverse_transform([pred_idx])[0]
        confidence = probs[0][pred_idx].item()

    if text == "/session_start":
        intent_name = "session_start"
        confidence = 1.0

    return {
        "intent": {"name": intent_name, "confidence": float(confidence)},
        "entities": entity_list,
        "text": text,
        "modtext": modtext
    }

# =============================================
# ENTITY + INTENT PIPELINE
# =============================================

def get_intent_and_entity(text):
    entities = hybrid_entity_recognition(text)
    entity_list = []
    modtext = text

    for ent in entities:
        entity_type = ent["entity"].upper()

        # Normalisasi entity ke slot RASA
        mapping = {
            "PER": "name",
            "EMAIL": "email",
            "JENJANG": "jenjang",
            "PRODI": "prodi",
            "FAKULTAS": "fakultas",
            "PROGRAM": "program"
        }
        entity_typex = mapping.get(entity_type, entity_type.lower())

        my_entity = {"value": ent["word"], "entity": entity_typex}
        entity_list.append(my_entity)

        # Modifikasi teks untuk prediksi intent (placeholder)
        if entity_typex in ["email", "jenjang", "prodi", "fakultas", "program"]:
            modtext = replace_entity(modtext, ent["word"], f"<{entity_typex}>")

    hasil = get_intent(text, model, tokenizer, label_encoder, entity_list, modtext)
    return hasil


# =============================================
# FLASK API ENDPOINT
# =============================================

@app.route("/model/parse", methods=["POST"])
def parse():
    data = request.get_json()
    user_input = data.g_
