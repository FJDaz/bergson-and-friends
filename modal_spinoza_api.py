"""
Modal Serverless API pour Spinoza (Qwen 2.5 14B + LoRA)
Charge le modèle depuis Modal Volume et expose API web
"""

import modal
from typing import List, Dict, Any

# Configuration
MODEL_NAME = "FJDaz/qwen-spinoza-niveau-b"
VOLUME_NAME = "spinoza-models"

# Créer l'app Modal
app = modal.App("spinoza-api")

# Monter le volume avec les modèles
volume = modal.Volume.from_name(VOLUME_NAME, create_if_missing=False)

# Image avec dépendances
image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "torch==2.1.0",
        "transformers==4.38.0",
        "accelerate==0.27.0",
        "bitsandbytes==0.42.0",
        "fastapi==0.109.0",
        "pydantic==2.6.0",
    )
)

# Classe Serverless pour l'inférence
@app.cls(
    gpu="A10G",
    image=image,
    volumes={"/models": volume},
    timeout=600,
    scaledown_window=120,  # Renamed from container_idle_timeout
)
class SpinozaModel:
    @modal.enter()
    def load_model(self):
        """Charge le modèle au démarrage du container"""
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        cache_dir = "/models"

        print(f"[LOAD] Loading model from {cache_dir}...")

        self.tokenizer = AutoTokenizer.from_pretrained(
            MODEL_NAME,
            cache_dir=cache_dir,
            local_files_only=True
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            cache_dir=cache_dir,
            local_files_only=True,
            torch_dtype=torch.float16,
            device_map="auto",
            load_in_8bit=True,  # Quantization 8-bit pour réduire VRAM
        )

        print("[LOAD] Model loaded!")

    @modal.method()
    def generate(
        self,
        message: str,
        history: List[List[str]] = None,
        max_tokens: int = 512,
        temperature: float = 0.7,
    ) -> str:
        """Génère une réponse de Spinoza"""
        import torch

        if history is None:
            history = []

        # Construire le prompt avec historique
        conversation = []

        # Ajouter l'historique
        for user_msg, assistant_msg in history:
            if user_msg:
                conversation.append(f"Question: {user_msg}")
            if assistant_msg:
                conversation.append(f"Spinoza: {assistant_msg}")

        # Ajouter le message actuel
        conversation.append(f"Question: {message}")
        conversation.append("Spinoza:")

        prompt = "\n\n".join(conversation)

        # Générer
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=True,
                top_p=0.9,
                pad_token_id=self.tokenizer.eos_token_id,
            )

        # Décoder et extraire la réponse
        full_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Extraire seulement la dernière réponse
        response = full_response.split("Spinoza:")[-1].strip()

        return response


# API Web FastAPI
@app.function(
    image=image,
    secrets=[],  # Ajoute tes secrets si besoin
)
@modal.web_endpoint(method="POST")
async def chat(request: Dict[str, Any]):
    """
    Endpoint HTTP pour chat

    POST /chat
    Body: {
        "message": "string",
        "history": [[user, assistant], ...],
        "max_tokens": 512,
        "temperature": 0.7
    }
    """
    from fastapi import HTTPException

    # Extraire les paramètres
    message = request.get("message")
    history = request.get("history", [])
    max_tokens = request.get("max_tokens", 512)
    temperature = request.get("temperature", 0.7)

    if not message:
        raise HTTPException(status_code=400, detail="Missing 'message' field")

    # Appeler le modèle
    model = SpinozaModel()
    response = model.generate.remote(
        message=message,
        history=history,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    return {
        "reply": response,
        "model": MODEL_NAME,
    }


# Endpoint de santé
@app.function(image=image)
@modal.web_endpoint(method="GET")
def health():
    """Health check endpoint"""
    return {
        "status": "ok",
        "model": MODEL_NAME,
        "provider": "modal",
    }


# Pour tester localement
@app.local_entrypoint()
def test():
    """Test local du modèle"""
    model = SpinozaModel()

    response = model.generate.remote(
        message="Qu'est-ce que la liberté selon toi?",
        history=[],
        max_tokens=200,
    )

    print(f"\n✅ Réponse de Spinoza:\n{response}\n")
