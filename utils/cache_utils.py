import os
import pickle
import json
from pathlib import Path

MODELS_CACHE_DIR = Path("/app/models_cache") if os.path.exists("/app/models_cache") else Path("./models_cache")

def ensure_cache_dir():
    """Asegura que el directorio de caché existe"""
    MODELS_CACHE_DIR.mkdir(exist_ok=True)

def get_model_cache_path(model_name):
    """Obtiene la ruta del caché para un modelo específico"""
    safe_name = model_name.replace("/", "_").replace("\\", "_")
    return MODELS_CACHE_DIR / safe_name

def save_model_to_cache(model_name, model_data):
    """Guarda un modelo y sus componentes en caché"""
    ensure_cache_dir()
    cache_path = get_model_cache_path(model_name)
    cache_path.mkdir(exist_ok=True)
    # Guardar cada componente por separado
    for component_name, component_data in model_data.items():
        component_path = cache_path / f"{component_name}.pkl"
        with open(component_path, 'wb') as f:
            pickle.dump(component_data, f)
    # Guardar metadatos
    metadata = {
        "model_name": model_name,
        "components": list(model_data.keys()),
        "cache_version": "1.0"
    }
    with open(cache_path / "metadata.json", 'w') as f:
        json.dump(metadata, f)
    print(f"Modelo {model_name} guardado en caché en: {cache_path}")

def load_model_from_cache(model_name: str) -> dict:
    """Carga un modelo desde el caché"""
    cache_path = get_model_cache_path(model_name)
    metadata_path = cache_path / "metadata.json"
    if not metadata_path.exists():
        return None
    try:
        # Cargar metadatos
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        # Cargar componentes
        model_data = {}
        for component_name in metadata["components"]:
            component_path = cache_path / f"{component_name}.pkl"
            if component_path.exists():
                with open(component_path, 'rb') as f:
                    model_data[component_name] = pickle.load(f)
            else:
                print(f"Componente {component_name} no encontrado en caché")
                return None
        print(f"Modelo {model_name} cargado desde caché: {cache_path}")
        return model_data
    
    except Exception as e:
        print(f"Error cargando modelo desde caché: {e}")
        return None

def is_model_cached(model_name):
    """Verifica si un modelo está en caché"""
    cache_path = get_model_cache_path(model_name)
    metadata_path = cache_path / "metadata.json"
    return metadata_path.exists()

def clear_model_cache(model_name = None):
    """Limpia el caché de un modelo específico o todo el caché"""
    if model_name:
        cache_path = get_model_cache_path(model_name)
        if cache_path.exists():
            import shutil
            shutil.rmtree(cache_path)
            print(f"Caché del modelo {model_name} eliminado")
    else:
        if MODELS_CACHE_DIR.exists():
            import shutil
            shutil.rmtree(MODELS_CACHE_DIR)
            MODELS_CACHE_DIR.mkdir(exist_ok=True)
            print("Todo el caché de modelos eliminado")
