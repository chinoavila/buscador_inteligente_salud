import dotenv
import os
from huggingface_hub import login
from transformers import AutoTokenizer, AutoModelForCausalLM, StoppingCriteria, StoppingCriteriaList, GenerationConfig
import streamlit as st
import json

# tomar Access Token de Hugging Face desde archivo .env
dotenv.load_dotenv() 
login(os.getenv("HF_TOKEN"))

class ListOfTokensStoppingCriteria(StoppingCriteria):
    """
    Clase para definir un criterio de parada basado en una lista de tokens específicos.
    """
    def __init__(self, tokenizer, stop_tokens):
        self.tokenizer = tokenizer
        # Codifica cada token de parada y guarda sus IDs en una lista
        self.stop_token_ids_list = [tokenizer.encode(stop_token, add_special_tokens=False) for stop_token in stop_tokens]

    def __call__(self, input_ids, scores, **kwargs):
        # Verifica si los últimos tokens generados coinciden con alguno de los conjuntos de tokens de parada
        for stop_token_ids in self.stop_token_ids_list:
            len_stop_tokens = len(stop_token_ids)
            if len(input_ids[0]) >= len_stop_tokens:
                if input_ids[0, -len_stop_tokens:].tolist() == stop_token_ids:
                    return True
        return False

@st.cache_resource
def load_model():
    """Carga los recursos de Hugging Face"""
    # Modelos probados:
    # https://huggingface.co/medicalai/ClinicalBERT
    # https://huggingface.co/emilyalsentzer/Bio_ClinicalBERT
    # https://huggingface.co/medalpaca/medalpaca-7b
    # https://huggingface.co/qanastek/MedAlpaca-LLaMa2-7B
    # https://huggingface.co/siddharthtumre/biobert-finetuned-ner
    # https://huggingface.co/somosnlp/Sam_Diagnostic

    model_id = "somosnlp/Sam_Diagnostic"

    tokenizer = AutoTokenizer.from_pretrained(model_id, max_length = 2048)
    stopping_criteria = ListOfTokensStoppingCriteria(tokenizer, ["<end_of_turn>"])
    stopping_criteria_list = StoppingCriteriaList([stopping_criteria])

    model = AutoModelForCausalLM.from_pretrained(model_id,
                                                attn_implementation = None
                                                ).eval()

    generation_config = GenerationConfig(
        max_new_tokens=2100,
        temperature=0.2,
        top_p=0.1, # reducir variabilidad
        top_k=50,
        repetition_penalty=1.,
        do_sample=True,
    )
    return tokenizer, model, generation_config, stopping_criteria, stopping_criteria_list

tokenizer, model, generation_config, stopping_criteria, stopping_criteria_list = load_model()

def cut_model_response(response_text):
    response_text = response_text.split("<start_of_turn>model")[1]
    final = response_text.find("<end_of_turn>")
    return response_text[:final]

def generate_with_hugging_face(prompt, input_lang_code, output_lang_code):
    # Fine-tunning
    input_text = f'''<bos>
    <start_of_turn>system
    You are a helpful AI assistant.
    Responde en formato JSON.
    Eres un agente experto en medicina.
    Lista de codigos linguisticos disponibles: ["{input_lang_code}", "{output_lang_code}"]
    <end_of_turn>
    <start_of_turn>user {prompt}<end_of_turn>
    <start_of_turn>model
    '''
    # Tokenizacion
    inputs = tokenizer.encode(input_text, return_tensors="pt", add_special_tokens=False)
    # Salidas codificadas
    outputs = model.generate(
        generation_config=generation_config,
        input_ids=inputs,
        stopping_criteria=stopping_criteria_list,)
    # Decodificacion
    response = tokenizer.decode(outputs[0], skip_special_tokens=False)
    # Formateo de respuesta
    return cut_model_response(response)