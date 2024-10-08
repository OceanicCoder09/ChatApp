import spacy
import random
from collections import defaultdict
import re

class AdvancedMedicalChatbot:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.knowledge_base = {
            "conditions": {
                "common cold": ["runny nose", "sore throat", "cough", "sneezing", "fatigue"],
                "flu": ["fever", "body aches", "fatigue", "cough", "headache"],
                "migraine": ["severe headache", "nausea", "sensitivity to light", "sensitivity to sound"],
                "allergies": ["sneezing", "itchy eyes", "runny nose", "congestion"],
                "hypertension": ["high blood pressure", "headache", "shortness of breath", "nosebleeds"],
                "diabetes": ["increased thirst", "frequent urination", "blurred vision", "fatigue"],
                "asthma": ["wheezing", "shortness of breath", "chest tightness", "coughing"],
                "depression": ["persistent sadness", "loss of interest", "sleep changes", "fatigue"],
                "anxiety": ["excessive worry", "restlessness", "difficulty concentrating", "sleep problems"],
                "arthritis": ["joint pain", "stiffness", "swelling", "reduced range of motion"],
                "cancer": ["unexplained weight loss", "fatigue", "fever", "pain"],
                "heart disease": ["chest pain", "shortness of breath", "irregular heartbeat", "fatigue"],
                "stroke": ["sudden numbness", "confusion", "trouble speaking", "severe headache"],
                "alzheimer's disease": ["memory loss", "confusion", "mood changes", "difficulty with daily tasks"],
                "parkinson's disease": ["tremor", "slowed movement", "rigid muscles", "impaired posture and balance"],
            },
            "drugs": {
                "acetaminophen": {
                    "uses": ["pain relief", "fever reduction"],
                    "side_effects": ["nausea", "liver damage (with high doses)"],
                    "precautions": ["avoid alcohol", "don't exceed recommended dose"]
                },
                "ibuprofen": {
                    "uses": ["pain relief", "inflammation reduction"],
                    "side_effects": ["stomach upset", "bleeding risk"],
                    "precautions": ["take with food", "avoid if you have stomach ulcers"]
                },
                "amoxicillin": {
                    "uses": ["bacterial infections"],
                    "side_effects": ["diarrhea", "rash"],
                    "precautions": ["finish entire prescription", "inform doctor of allergies"]
                },
                "lisinopril": {
                    "uses": ["high blood pressure", "heart failure"],
                    "side_effects": ["dizziness", "cough"],
                    "precautions": ["monitor blood pressure", "avoid pregnancy"]
                },
                "metformin": {
                    "uses": ["type 2 diabetes"],
                    "side_effects": ["nausea", "diarrhea"],
                    "precautions": ["regular blood sugar monitoring", "avoid with kidney problems"]
                },
                "atorvastatin": {
                    "uses": ["high cholesterol"],
                    "side_effects": ["muscle pain", "liver problems"],
                    "precautions": ["avoid grapefruit", "regular liver function tests"]
                },
                "sertraline": {
                    "uses": ["depression", "anxiety"],
                    "side_effects": ["nausea", "sexual dysfunction"],
                    "precautions": ["avoid alcohol", "don't stop abruptly"]
                }
            },
            "general_advice": [
                "Maintain a balanced diet with plenty of fruits and vegetables.",
                "Stay hydrated by drinking enough water throughout the day.",
                "Get regular exercise, aiming for at least 150 minutes of moderate activity per week.",
                "Ensure you get enough sleep, typically 7-9 hours for adults.",
                "Manage stress through relaxation techniques like meditation or deep breathing exercises.",
                "Keep up with regular health check-ups and screenings.",
                "Practice good hygiene, including regular handwashing.",
                "Limit alcohol consumption and avoid smoking.",
                "Wear sunscreen and protect your skin from excessive sun exposure.",
                "Stay up to date on vaccinations.",
                "Practice mindfulness and meditation to improve mental health.",
                "Maintain social connections and engage in community activities.",
                "Limit screen time and practice good digital hygiene.",
                "Practice good posture and ergonomics, especially if you work at a desk.",
                "Stay mentally active by learning new skills or engaging in puzzles and games.",
                "Practice safe sex and get regular STI screenings if sexually active.",
                "Maintain good oral hygiene with regular brushing, flossing, and dental check-ups.",
                "Stay informed about your family health history and discuss it with your doctor.",
                "Practice safe driving habits, including wearing a seatbelt and avoiding distractions.",
                "Be aware of your mental health and seek help if you're struggling."
            ],
            "first_aid": {
                "cuts and scrapes": "Clean the wound with soap and water, apply antibiotic ointment, and cover with a sterile bandage.",
                "burns": "Run cool water over the burn for at least 10 minutes. Cover with a clean, dry dressing.",
                "sprains": "Follow the RICE method: Rest, Ice, Compression, and Elevation.",
                "choking": "Perform the Heimlich maneuver if the person can't breathe, cough, or speak.",
                "heart attack": "Call emergency services immediately. Have the person chew and swallow an aspirin if available.",
                "stroke": "Remember FAST: Face drooping, Arm weakness, Speech difficulty, Time to call emergency services.",
                "allergic reaction": "If severe, use an epinephrine auto-injector if available and seek immediate medical help.",
                "fractures": "Immobilize the injured area and seek medical attention. Don't attempt to realign the bone.",
                "poisoning": "Call poison control immediately. Do not induce vomiting unless instructed by a professional.",
                "heat exhaustion": "Move to a cool place, drink water, and apply cool, wet cloths to the body."
            },
            "nutrition": {
                "protein": ["meat", "fish", "eggs", "legumes", "dairy"],
                "carbohydrates": ["whole grains", "fruits", "vegetables", "legumes"],
                "fats": ["avocado", "nuts", "seeds", "olive oil", "fatty fish"],
                "vitamins": {
                    "A": ["carrots", "sweet potatoes", "spinach"],
                    "C": ["citrus fruits", "berries", "bell peppers"],
                    "D": ["sunlight", "fatty fish", "egg yolks"],
                    "E": ["almonds", "sunflower seeds", "avocados"]
                },
                "minerals": {
                    "iron": ["red meat", "spinach", "lentils"],
                    "calcium": ["dairy products", "leafy greens", "sardines"],
                    "magnesium": ["nuts", "seeds", "whole grains"]
                }
            }
        }

    def get_response(self, user_input):
        doc = self.nlp(user_input.lower())
        
        # Check for greetings
        greetings = ["hello", "hi", "hey", "greetings"]
        if any(greeting in user_input.lower() for greeting in greetings):
            return "Hello! How can I assist you with your health-related questions today?"
        
        # Check for condition names directly
        for condition in self.knowledge_base["conditions"]:
            if condition in user_input.lower():
                symptoms = ", ".join(self.knowledge_base["conditions"][condition])
                return f"The common symptoms of {condition} include: {symptoms}. Please consult a healthcare professional for a proper diagnosis."
        
        # Check for symptom-related queries
        if any(token.text in ["symptom", "symptoms", "feeling", "experiencing"] for token in doc):
            return self.check_symptoms(doc)
        
        # Check for drug-related queries
        if any(token.text in ["drug", "medication", "medicine"] for token in doc):
            return self.provide_drug_info(doc)
        
        # Check for general health advice
        if any(token.text in ["advice", "tips", "recommendation"] for token in doc):
            return self.give_general_advice()
        
        # Check for first aid information
        if "first aid" in user_input.lower() or any(situation in user_input.lower() for situation in self.knowledge_base["first_aid"]):
            return self.provide_first_aid_info(user_input)
        
        # Check for nutrition information
        if any(token.text in ["nutrition", "diet", "food", "eat", "eating"] for token in doc):
            return self.provide_nutrition_info(doc)
        
        # If no specific category is detected, check for drug names directly
        drug_info = self.provide_drug_info(doc)
        if drug_info != "I couldn't find information about the specific drug you mentioned. Please check the spelling or ask about a different medication.":
            return drug_info
        
        # Default response for unrecognized queries
        return "I'm not sure how to respond to that. Could you please rephrase your question or ask about symptoms, medications, first aid, nutrition, or general health advice?"

    def check_symptoms(self, doc):
        reported_symptoms = [token.text for token in doc if token.pos_ == "NOUN" or token.pos_ == "ADJ"]
        possible_conditions = defaultdict(int)

        for condition, symptoms in self.knowledge_base["conditions"].items():
            for symptom in symptoms:
                if any(word in symptom for word in reported_symptoms):
                    possible_conditions[condition] += 1

        if possible_conditions:
            most_likely = max(possible_conditions, key=possible_conditions.get)
            return f"Based on the symptoms you've described, it's possible you may have {most_likely}. However, please consult with a healthcare professional for an accurate diagnosis. Remember that many conditions can have similar symptoms, and only a qualified medical professional can provide a proper diagnosis."
        else:
            return "I couldn't identify any specific condition based on the information provided. It's best to consult with a healthcare professional for personalized advice. They can perform a thorough examination and consider your full medical history."

    def provide_drug_info(self, doc):
        drug_names = [token.text for token in doc if token.text in self.knowledge_base["drugs"]]
        
        if drug_names:
            drug = drug_names[0]
            info = self.knowledge_base["drugs"][drug]
            return f"Information about {drug}:\nUses: {', '.join(info['uses'])}\nSide effects: {', '.join(info['side_effects'])}\nPrecautions: {', '.join(info['precautions'])}\n\nPlease note that this is general information. Always consult with a healthcare professional or pharmacist for personalized advice about medications."
        else:
            return "I couldn't find information about the specific drug you mentioned. Please check the spelling or ask about a different medication. Remember, it's always best to consult with a healthcare professional or pharmacist for accurate and personalized medication information."

    def give_general_advice(self):
        advice = random.sample(self.knowledge_base["general_advice"], 3)
        return "Here are some general health tips:\n\n" + "\n".join(f"- {tip}" for tip in advice) + "\n\nRemember, these are general suggestions. For personalized advice, consult with a healthcare professional."

    def provide_first_aid_info(self, user_input):
        for situation, instructions in self.knowledge_base["first_aid"].items():
            if situation in user_input.lower():
                return f"First aid for {situation}: {instructions}\n\nRemember, in case of severe injuries or life-threatening situations, always call emergency services immediately."
        return "I couldn't find specific first aid information for that situation. For any medical emergency, it's best to call emergency services or consult a healthcare professional."

    def provide_nutrition_info(self, doc):
        nutrition_keywords = ["protein", "carbohydrates", "fats", "vitamins", "minerals"]
        for keyword in nutrition_keywords:
            if keyword in [token.text for token in doc]:
                if keyword in ["vitamins", "minerals"]:
                    info = "\n".join([f"{nutrient}: {', '.join(sources)}" for nutrient, sources in self.knowledge_base["nutrition"][keyword].items()])
                else:
                    info = ", ".join(self.knowledge_base["nutrition"][keyword])
                return f"Good sources of {keyword} include: {info}\n\nRemember to maintain a balanced diet and consult with a nutritionist for personalized advice."
        return "For good nutrition, aim for a balanced diet including a variety of fruits, vegetables, whole grains, lean proteins, and healthy fats. If you have specific dietary concerns or requirements, it's best to consult with a registered dietitian or nutritionist."

    def chat(self):
        print("Advanced Medical Assistant: Hello! I'm here to provide general medical information, check symptoms, offer drug information, give first aid advice, and discuss nutrition. What can I help you with today?")
        print("(Type 'quit' to exit)")

        while True:
            user_input = input("You: ").strip()
            if user_input.lower() == 'quit':
                print("Advanced Medical Assistant: Take care! Remember to consult with a healthcare professional for personalized medical advice.")
                break
            
            response = self.get_response(user_input)
            print("Advanced Medical Assistant:", response)

if __name__ == "__main__":
    chatbot = AdvancedMedicalChatbot()
    chatbot.chat()