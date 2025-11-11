# =============================================================================
# SCRIPT CURSOR - CORRECTION HUGGINGFACE SPACE API
# Fichier: hf-space/app.py (à déployer sur ton Space HuggingFace)
# =============================================================================

import gradio as gr

def spinoza_chat(message, history):
    """
    Fonction temporaire pour tester l'API
    TODO: Remplacer par ton vrai modèle une fois l'API validée
    """
    
    # Réponse test pour valider l'API
    response = f"""🎭 **Spinoza** : Salut ! Je reçois bien ton message "{message}". 

L'API REST fonctionne correctement. Prochaine étape : intégrer le vrai modèle fine-tuné !

*[Message de test - API validée]*"""
    
    return response

# =============================================================================
# CONFIGURATION GRADIO AVEC API ACTIVÉE
# =============================================================================

demo = gr.ChatInterface(
    fn=spinoza_chat,
    title="🧠 Bergson & Friends - Spinoza",
    description="Test API REST - Dialogue avec Spinoza",
    examples=[
        "Qu'est-ce que la substance ?",
        "Comment définissez-vous les affects ?",
        "L'API fonctionne-t-elle ?"
    ],
    retry_btn="🔄 Retry",
    undo_btn="↩️ Undo", 
    clear_btn="🗑️ Clear"
)

# CRUCIAL: Configuration qui active l'API REST
demo.queue(
    api_open=True,          # ← CLÉE : Active l'API REST
    max_size=20,            # Limite queue
    concurrency_count=3     # Requêtes simultanées
)

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        show_api=True,         # ← Documentation API sur /docs
        share=False
    )