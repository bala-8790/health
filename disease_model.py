# disease_model.py
def predict_disease(symptoms):
    disease_map = {
        "Fever": ["Dengue", "Malaria", "Typhoid", "COVID-19"],
        "Cough": ["TB", "COVID-19", "Flu"],
        "Fatigue": ["Diabetes", "HIV/AIDS", "Cancer"],
        "Weight Loss": ["Thyroid", "TB", "Cancer"],
        "Headache": ["Migraine", "Brain Tumor", "Flu"],
        "Rash": ["Chickenpox", "Dengue"],
        "Sweating": ["Malaria", "Anemia"],
        "Joint Pain": ["Dengue", "Chikungunya"],
        "Chest Pain": ["Heart Disease", "Lung Infection"],
        "Blood in Cough": ["TB", "Lung Cancer"],
        "Vomiting": ["Typhoid", "Gastroenteritis"],
    }

    disease_score = {}
    for symptom in symptoms:
        possible_diseases = disease_map.get(symptom, [])
        for disease in possible_diseases:
            disease_score[disease] = disease_score.get(disease, 0) + 1

    sorted_diseases = sorted(disease_score.items(), key=lambda x: x[1], reverse=True)
    return [d[0] for d in sorted_diseases[:3]]
