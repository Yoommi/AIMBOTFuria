import requests
from datetime import datetime

# ajuste de data e hora PT-BR
def formatar_data(data_iso):
    if not data_iso:
        return "Data indefinida"
    
    try:
        data = datetime.fromisoformat(data_iso.replace("Z", "+00:00"))
        return data.strftime("%d/%m/%Y - %H:%M")
    except Exception as e:
        print(f"Erro ao formatar data: {e}")
        return "Data inválida"

# API do Pandascore
API_KEY = "faOa5wv2NiDEdpS_4KbK7X4QNkjxjpF7PBwXIhhbtdJxDb353J8"

# próximos jogos
def buscar_proximos_jogos_furia():
    try:
        # URL com filtro para o time da FURIA
        url = f"https://api.pandascore.co/csgo/matches/upcoming?search[team_name]=furia&token={API_KEY}"
        
        response = requests.get(url)
        response.raise_for_status()

        partidas = response.json()

        if not partidas:
            return "🚫 Opa, parece que não jogamos nos próximos dias."

        mensagem = "🔥 Prontinho, aqui estãos nossos próximos jogos:\n\n"

        for partida in partidas[:5]:  # Limita para mostrar no máximo 5 partidas
            adversario = partida['opponents'][1]['opponent']['name'] if len(partida['opponents']) > 1 else "Adversário indefinido"
            data = partida['begin_at']
            campeonato = partida['tournament']['name']

            mensagem += f"🏆 Campeonato: {campeonato}\n"
            mensagem += f"🆚 Adversário: {adversario}\n"
            mensagem += f"🗓️ Data: {data}\n\n"

        return mensagem

    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar partidas: {e}")
        return "🚨 Não consegui buscar as partidas, pode tentar novamente mais tarde?."