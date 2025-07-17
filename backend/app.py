import google.generativeai as genai
import os
from flask import Flask, request, jsonify
import json
from flask_cors import CORS
import time
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app) 



@app.route('/generate', methods=['POST'])
def generate_ideas():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Nenhum dado recebido"}), 400
    system_info = data.get('systemInfo')
    qtd_ideias = data.get('ideaCount')

    # with open('backend/dados/dados_sistema.txt', 'w', encoding='utf-8') as f:
    #   f.write(system_info)


    # Configura a API key a partir da variável de ambiente
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

    # Seleciona o modelo a ser utilizado
    # 'gemini-1.5-flash' é um modelo rápido e eficiente
    model = genai.GenerativeModel('gemini-1.5-flash')
    chat = model.start_chat(history=[])


    response = chat.send_message("O que é um brainstorm no contexto de engenharia de requisitos?")

    prompt = f"""
    [TAREFA]
    Crie 6 perfis de stakeholders para um projeto de software, incluindo nome, cargo, responsabilidades e interesses,
    com personalidades distintas e características únicas. o sistem_info é um texto que contém informações sobre o sistema.

    [INFORMAÇÕES DO SISTEMA]
    {system_info}
    """

    response = chat.send_message(prompt)

    prompt = f"""
    [TAREFA]
    Simule um brainstorm com os 6 perfis de stakeholders criados anteriormente, gere ideias criativas e sem filtros
    como se fosse uma reunião presencial, com discussões e interações entre os participantes.
    [INFORMAÇÕES DO SISTEMA]
    {system_info}
    """

    response = chat.send_message(prompt)

    prompt = f"""
    [TAREFA]
    Agora, Categorize as ideias geradas para selecionar as mais viáveis e relevantes para o projeto, considerando viabilidade técnica, 
    impacto no usuário e alinhamento com os objetivos do sistema.
    [INFORMAÇÕES DO SISTEMA]
    {system_info}
    """
    response = chat.send_message(prompt)

    prompt = f"""
    [TAREFA]
    Crie uma lista com a quantidade de ideias indicadada por {qtd_ideias} ideias, com base nas ideias categorizadas anteriormente. 
    a saída deverá conter somente o nome da ideia e uma breve descrição, sem explicações adicionais.
    [QUANTIDADE DE IDEIAS]
    {qtd_ideias}

    """
    response = chat.send_message(prompt)

    # Ler o conteúdo do arquivo e retornar como resposta JSON
    # with open('backend/dados/resultado.txt', 'w', encoding='utf-8') as f:
    #    f.write(response.text)

    return jsonify({
        "generated_ideas": response.text
    })
if __name__ == '__main__':
    # debug=True faz o servidor reiniciar automaticamente quando você altera o código
    app.run(host='0.0.0.0', port=5000, debug=True)
