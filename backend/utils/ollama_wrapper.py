import ollama

def call_local_model(prompt: str, model: str = "mistral") -> str:
    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response['message']['content'].strip()
