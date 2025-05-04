import requests

API_KEY = "faOa5wv2NiDEdpS_4KbK7X4QNkjxjpF7PBwXIhhbtdJxDb353J8"

def estatisticas_do_jogador():
    try:
        url = f"https://api.pandascore.co/csgo/teams?search[name]=furia&token={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()

        times = response.json()

        if not times:
            return "Desculpe, não achei nosso time."

        furia = times[0]  # Pega o primeiro time que bater o nome
        jogadores = furia['players']

        mensagem = "👥 Jogadores da FURIA:\n\n"

        for jogador in jogadores:
            nome = jogador['name']
            nickname = jogador['slug']
            role = jogador.get('role', 'Função não informada')

            mensagem += f"{nome} ({nickname})\n"
            mensagem += f"Função: {role}\n\n"

        return mensagem

    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar jogadores: {e}")
        return "Erro ao buscar jogadores no momento."
