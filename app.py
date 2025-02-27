from flask import Flask, request, jsonify, send_file
import json
import os

app = Flask(__name__)

# Load the livestock database
LIVESTOCK_DATA = {
    "goat": {
        "symptoms": [
            "Diarrhea", "Coughing", "Weight loss", "Fever", "Lethargy",
            "Poor appetite", "Bloating", "Limping", "Hair loss", "Skin lesions",
            "Nasal discharge", "Difficulty breathing", "Swollen joints", "Anemia (pale gums)",
            "Abnormal milk", "Abortion", "Head tilting", "Grinding teeth", "Excessive salivation"
        ],
        "diseases": {
            "Coccidiosis": {
                "symptoms": ["Diarrhea", "Weight loss", "Lethargy", "Poor appetite"],
                "treatments": [
                    "Administer anticoccidial medication such as Amprolium (Corid) as prescribed by a veterinarian",
                    "Ensure clean water and feed to prevent reinfection",
                    "Isolate affected animals to prevent spread",
                    "Provide supportive care with electrolytes to prevent dehydration"
                ],
                "prevention": [
                    "Maintain clean and dry housing",
                    "Avoid overcrowding",
                    "Elevate feed and water containers to prevent fecal contamination",
                    "Proper manure management and regular cleaning of pens",
                    "Consider prophylactic treatment in high-risk environments"
                ]
            },
            # Add more diseases as needed
        }
    },
    "cattle": {
        "symptoms": [
            "Diarrhea", "Coughing", "Weight loss", "Fever", "Lethargy",
            "Reduced milk production", "Bloating", "Lameness", "Hair loss", "Increased respiratory rate",
            "Nasal discharge", "Difficulty breathing", "Swollen joints", "Anemia (pale mucous membranes)",
            "Abnormal milk", "Abortion", "Decreased rumen activity", "Excessive salivation", "Loss of appetite"
        ],
        "diseases": {
            "Bovine Respiratory Disease (BRD)": {
                "symptoms": ["Coughing", "Fever", "Nasal discharge", "Increased respiratory rate", "Lethargy"],
                "treatments": [
                    "Administer appropriate antibiotics as prescribed by a veterinarian",
                    "Anti-inflammatory medications to reduce fever and inflammation",
                    "Provide adequate rest and reduced stress",
                    "Ensure good ventilation and comfortable housing"
                ],
                "prevention": [
                    "Vaccination against common respiratory pathogens",
                    "Proper ventilation in housing",
                    "Gradual introduction to new environments",
                    "Reduce stress during handling and transportation",
                    "Isolate new or sick animals"
                ]
            },
            # Add more diseases as needed
        }
    }
}

@app.route('/')
def index():
    # Serve the HTML file directly from the same folder
    return send_file('index.html')

@app.route('/api/symptoms', methods=['GET'])
def get_symptoms():
    animal_type = request.args.get('animal_type')
    if animal_type in LIVESTOCK_DATA:
        return jsonify({"symptoms": LIVESTOCK_DATA[animal_type]["symptoms"]})
    return jsonify({"error": "Invalid animal type"}), 400

@app.route('/api/diseases', methods=['GET'])
def get_diseases():
    animal_type = request.args.get('animal_type')
    if animal_type in LIVESTOCK_DATA:
        return jsonify({"diseases": LIVESTOCK_DATA[animal_type]["diseases"]})
    return jsonify({"error": "Invalid animal type"}), 400

@app.route('/api/diagnose', methods=['POST'])
def diagnose():
    data = request.json
    animal_type = data.get('animal_type')
    symptoms = data.get('symptoms', [])
    age = data.get('age')
    notes = data.get('notes', '')
    
    if not animal_type or not symptoms or not age:
        return jsonify({"error": "Missing required data"}), 400
    
    if animal_type not in LIVESTOCK_DATA:
        return jsonify({"error": "Invalid animal type"}), 400
    
    # Find matching diseases
    matching_diseases = {}
    diseases = LIVESTOCK_DATA[animal_type]["diseases"]
    
    for disease_name, disease_info in diseases.items():
        matching_symptoms = [s for s in disease_info["symptoms"] if s in symptoms]
        if matching_symptoms:
            match_percentage = (len(matching_symptoms) / len(disease_info["symptoms"])) * 100
            matching_diseases[disease_name] = {
                "match_percentage": round(match_percentage),
                "matching_symptoms": matching_symptoms,
                "treatments": disease_info["treatments"],
                "prevention": disease_info["prevention"]
            }
    
    # Sort diseases by match percentage
    sorted_diseases = sorted(
        matching_diseases.items(),
        key=lambda x: x[1]["match_percentage"],
        reverse=True
    )
    
    result = {
        "animal": animal_type,
        "age": age,
        "matching_diseases": dict(sorted_diseases),
        "top_match": sorted_diseases[0][0] if sorted_diseases else None
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)