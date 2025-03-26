import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

def generate(frase):
    history = load_chat()
    # Certifique-se de definir corretamente a chave API
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("A chave de API não foi encontrada no ambiente ou no código.")

    # Cliente do Gemini
    client = genai.Client(api_key=api_key)

    model = "gemini-2.0-flash"

    # Histórico de interações
    initial_content = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text="""
        Você é um chatbot especializado em marketing digital.
        **Suas respostas devem ser curtas e diretas até ter toda informação para montar o texto.**
        Evite explicações longas e só forneça detalhes de acordo com o que  o usuário pedir.""")],
        ),
        types.Content(
            role="model",
            parts=[types.Part.from_text(text="""{
        "role": "Chatbot especializado em marketing digital",
        "function": "Gerar textos criativos e adaptados para campanhas de marketing digital...",
        "abilities": ["Adaptar o tom e estilo de escrita...", "Gerar ideias criativas..."],
        "language": "Português do Brasil",
        "goal": "Fornecer um texto por comando de marketing digital eficazes e personalizados após ter todas as informações",
        "emphasis": "Criatividade, adaptação, persuasão e foco no público-alvo."
        }""")],
        ),]

    # Adiciona a nova interação do usuário
    contents = initial_content + history
        # types.Content(
        #     role="user",
        #     parts=[types.Part.from_text(text=frase)],  # Corrigido aqui!
        # ),
    contents.append(
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=frase)],
        ),
    )

    # Configuração do modelo
    generate_content_config = types.GenerateContentConfig(
        temperature=1.3,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        response_mime_type="text/plain",
    )

    # Gerar conteúdo com base no histórico
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config
    )
    save_chat(frase)
    return response.text  # Retorn   ando a resposta gerada corretamente


def load_chat():
    try:
        with open("Desktop/Trabalho-eficaz/Assets/Script/chats.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        print("ERROR ao carregar json")
        print(exc)
        return []
    
    
def save_chat(historico):

    current_history = load_chat()
    current_history.append(historico)

    with open("Desktop/Trabalho-eficaz/Assets/Script/chats.json", "w") as file:
        json.dump(current_history, file,  indent=4, ensure_ascii=False)

while True:
    var = str(input("Digite: "))
    print(generate(var))