import json
from dotenv import load_dotenv
import google.generativeai as genAI
from load_creds import load_creds


load_dotenv()

creds = load_creds()

# ------ insert LLM 
genAI.configure()

tuned_model_name = 'tunedModels/actiontestcolors3-2lyoseyl2q2s'
# tuned_model_name = 'tunedModels/knowledge2-yaqx10fkkdqx'

generation_config = {
    'temperature': 0.1,
    'top_p': .5,
    'top_k': 1,
    'max_output_tokens': 1000,
}

safety_settings = []

AI_model = genAI.GenerativeModel(model_name=tuned_model_name, generation_config=generation_config, safety_settings=safety_settings)

def get_ft_response(question: str):
    if question == '':
        response = [customRes('Es ist schwer auf eine leere Frage die richtige Antwort zu finden :)'), {'action': False, 'params': ''}]
        return response
    response = AI_model.generate_content(question)
    task = {'action' : False, 'params': {}}
    return [response, task]

class customRes:
    def __init__(self, text):
        self.text = text

def change_color(color: str):
    with open('./frontend/assets/styles/color.css', 'w') as file:
        file.write(f"html {{ --clr-accent: {color}; }}")

with open('./frontend/assets/styles/color.css', 'w') as file:
    file.write(f"html {{ --clr-accent: #ff004d; }}")