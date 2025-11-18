import gradio as gr
from gradio_client import Client

SNB_SPACE = "FJDaz/spinoza_NB"

client = Client(SNB_SPACE)

API_NAMES = {
    "spinoza": "/chat_spinoza",
    "bergson": "/chat_bergson",
    "kant": "/chat_kant",
}

def orchestrate(philosopher, message, history):
    if not message:
        return "", history or []

    api_name = API_NAMES.get(philosopher, "/chat_spinoza")

    result = client.predict(
        message=message,
        history=history or [],
        api_name=api_name,
    )
    reply, new_history = result  # (str, history)
    return reply, new_history

demo = gr.Interface(
    fn=orchestrate,
    inputs=[
        gr.Dropdown(["spinoza", "bergson", "kant"], value="spinoza", label="Philosophe"),
        gr.Textbox(label="Message de l'élève"),
        gr.State(),
    ],
    outputs=[
        gr.Textbox(label="Réponse du philosophe"),
        gr.State(),
    ],
    title="SNB Orchestrator (proxy)",
    description="Proxy vers le Space FJDaz/spinoza_NB pour Spinoza, Bergson et Kant.",
    api_name="/orchestrate",
)

if __name__ == "__main__":
    demo.queue()
    demo.launch(show_api=True)
