import os
#import dotenv
#from huggingface_hub import login
import importlib
import requests
import streamlit as st

# # tomar Access Token de Hugging Face desde archivo .env
# dotenv.load_dotenv()
# login(os.getenv("HF_TOKEN"))

@st.cache_resource
def load_model():
    """Carga los recursos de Hugging Face"""
    transformers = importlib.import_module("transformers")
    AutoTokenizer = transformers.AutoTokenizer
    AutoModelForCausalLM = transformers.AutoModelForCausalLM
    StoppingCriteria = transformers.StoppingCriteria
    StoppingCriteriaList = transformers.StoppingCriteriaList
    GenerationConfig = transformers.GenerationConfig

    class ListOfTokensStoppingCriteria(StoppingCriteria):
        """Criterio de parada basado en una lista de tokens específicos."""
        def __init__(self, tokenizer, stop_tokens):
            self.tokenizer = tokenizer
            self.stop_token_ids_list = [
                tokenizer.encode(stop_token, add_special_tokens=False) for stop_token in stop_tokens
            ]

        def __call__(self, input_ids, scores, **kwargs):
            for stop_token_ids in self.stop_token_ids_list:
                len_stop_tokens = len(stop_token_ids)
                if len(input_ids[0]) >= len_stop_tokens:
                    if input_ids[0, -len_stop_tokens:].tolist() == stop_token_ids:
                        return True
            return False

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


def _remote_mode_enabled():
    """Devuelve True si está configurada una URL de Endpoint remoto de HF."""
    return os.getenv("HF_ENDPOINT_URL")


# Cargar el modelo solo si NO estamos en modo remoto 
# Esto evita descargas innecesarias
if _remote_mode_enabled():
    tokenizer = None
    model = None
    generation_config = None
    stopping_criteria = None
    stopping_criteria_list = None
else:
    tokenizer, model, generation_config, stopping_criteria, stopping_criteria_list = load_model()

def cut_model_response(response_text):
    response_text = response_text.split("<start_of_turn>model")[1]  
    final = response_text.find("<end_of_turn>")
    return response_text[:final]

def generate_with_hf_endpoint(input_text: str) -> str:
    """Llama a un Hugging Face Inference Endpoint con el mismo prompt y parámetros.

    Requiere variables de entorno:
    - HF_ENDPOINT_URL: URL del endpoint de HF
    - HF_TOKEN: token de acceso a HF
    """
    url = os.getenv("HF_ENDPOINT_URL")
    token = os.getenv("HF_TOKEN")
    if not url:
        raise RuntimeError("HF_ENDPOINT_URL no está definido en el entorno.")
    if not token:
        raise RuntimeError("HF_TOKEN no está definido en el entorno.")

    params = {
        "max_new_tokens": 2100,
        "temperature": 0.2,
        "top_p": 0.1,
        "top_k": 50,
        "repetition_penalty": 1.0,
        "do_sample": True,
        "return_full_text": True,
        "stop": ["<end_of_turn>"], # Reemplazo del stopping_criteria_list local
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    payload = {
        "inputs": input_text,
        "parameters": params,
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=120)
    resp.raise_for_status()
    data = resp.json()

    # TGI/Endpoints suelen devolver una lista con generated_text
    generated = None
    if isinstance(data, list) and data:
        item = data[0]
        generated = item.get("generated_text") or item.get("generated_texts")
    elif isinstance(data, dict):
        generated = data.get("generated_text")

    if not generated:
        raise RuntimeError(f"Respuesta inesperada del endpoint HF: {data}")

    return generated

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
    # Modo remoto (HF Inference Endpoint)
    response = None
    if _remote_mode_enabled():
        response = generate_with_hf_endpoint(input_text)
    else:
        # Modo local (transformers)
        # Tokenizacion
        inputs = tokenizer.encode(input_text, return_tensors="pt", add_special_tokens=False)
        # Salidas codificadas
        outputs = model.generate(
            generation_config=generation_config,
            input_ids=inputs,
            stopping_criteria=stopping_criteria_list,
        )
        # Decodificacion
        response = tokenizer.decode(outputs[0], skip_special_tokens=False)
    # Formateo de respuesta
    return cut_model_response(response)