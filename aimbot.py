# -*- coding: utf-8 -*-

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)
import requests
from bs4 import BeautifulSoup
import json
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações do ambiente
MODO_DEVELOPMENT = True  # Altere para False para usar dados reais
DADOS_EXEMPLO = "dados_exemplo.json"

# Constantes e configurações
SALVAR_NOMES = "nomes.json"  # Arquivo para armazenar os nomes dos usuários
fãs = {}  # Dicionário para armazenar os nomes dos usuários em memória

def carregar_dados_exemplo():
    """
    Carrega os dados de exemplo do arquivo JSON.
    Retorna um dicionário com os dados ou None em caso de erro.
    """
    try:
        with open(DADOS_EXEMPLO, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Arquivo {DADOS_EXEMPLO} não encontrado.")
        return None
    except json.JSONDecodeError:
        print(f"Erro ao decodificar o arquivo {DADOS_EXEMPLO}.")
        return None

def salvar():
    """
    Salva o dicionário de nomes dos usuários em um arquivo JSON.
    Utiliza encoding UTF-8 para suportar caracteres especiais.
    """
    with open(SALVAR_NOMES, "w", encoding="utf-8") as f:
        json.dump(fãs, f, ensure_ascii=False, indent=4)

def buscar_nomes():
    """
    Carrega os nomes dos usuários do arquivo JSON para a memória.
    Se o arquivo não existir, inicia um dicionário vazio.
    """
    global fãs
    try:
        with open(SALVAR_NOMES, "r", encoding="utf-8") as f:
            fãs = json.load(f)
    except FileNotFoundError:
        fãs = {}

buscar_nomes()

# Estados da conversa para o ConversationHandler
ASKING_NAME, SELECT_OPTIONS = range(2)

# Mensagens padrão do bot
MENU_MESSAGE = (
    "Como posso te ajudar hoje?\n\n"
    "Escreva uma das opções abaixo:\n"
    "- Campeonatos\n"
    "- Próximos Jogos\n"
    "- Estatísticas do Time\n"
    "- Estatísticas de um Jogador\n"
    "- Produtos\n"
    "- Redes Sociais\n"
    "- Menu"
)

HELP_MESSAGE = (
    "Comandos disponíveis:\n"
    "/start - Iniciar o bot\n"
    "/help - Mostrar esta mensagem de ajuda\n"
    "/menu - Voltar ao menu principal"
)

# início da conversa
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Inicia a conversa com o usuário, pedindo seu nome.
    Retorna o estado ASKING_NAME para continuar o fluxo da conversa.
    """
    await update.message.reply_text("Saudações, Furioso!\n\nQual o seu nome ou como gostaria de ser chamado?")
    return ASKING_NAME

async def pegar_nome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Armazena o nome do usuário e apresenta o menu principal.
    Salva o nome no arquivo JSON para persistência.
    """
    nome = update.message.text
    user_id = update.effective_user.id

    fãs[user_id] = nome
    salvar()

    await update.message.reply_text(
        f"Muito Prazer, {nome}! Eu sou o AIMBot, mas juro que sou amigável e não trapaceio 😁\n\n"
        f"{MENU_MESSAGE}"
    )
    return SELECT_OPTIONS

# menu
async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Gerencia as opções do menu principal.
    Direciona o usuário para a função correspondente à opção escolhida.
    """
    user_message = update.message.text.lower().strip()
    
    if user_message == "campeonatos":
        await campeonatos(update, context)
    elif user_message == "próximos jogos":
        await proximos_jogos(update, context)
    elif user_message == "estatísticas do time":
        await estatisticas_do_time(update, context)
    elif user_message == "estatísticas de um jogador":
        await estatisticas_do_jogador(update, context)
    elif user_message == "produtos":
        await loja(update, context)
    elif user_message == "redes sociais":
        await redes_sociais(update, context)
    elif user_message == "menu":
        await update.message.reply_text(MENU_MESSAGE)
    else:
        await update.message.reply_text(
            "Opção inválida. Por favor, escolha uma das opções abaixo:\n\n" + 
            MENU_MESSAGE
        )
    return SELECT_OPTIONS

async def campeonatos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Busca e exibe informações sobre os próximos campeonatos da Fúria.
    Utiliza web scraping para obter dados do site HLTV.org ou dados de exemplo.
    """
    try:
        if MODO_DEVELOPMENT:
            dados = carregar_dados_exemplo()
            if dados and "campeonatos" in dados:
                message = "🏆 Próximos Campeonatos da Fúria:\n\n"
                for campeonato in dados["campeonatos"]:
                    message += f"📅 {campeonato['data']}\n"
                    message += f"🏆 {campeonato['nome']}\n"
                    message += f"📍 {campeonato['local']}\n"
                    message += f"💰 {campeonato['premio']}\n"
                    message += "───────────────\n"
            else:
                message = "Não há campeonatos agendados no momento.\n"
        else:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get('https://www.hltv.org/team/8297/furia', headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            message = "🏆 Próximos Campeonatos da Fúria:\n\n"
            
            events = soup.find_all('div', {'class': 'event'})
            if events:
                for event in events[:5]:
                    event_name = event.find('div', {'class': 'event-name'})
                    event_date = event.find('div', {'class': 'event-date'})
                    
                    if event_name and event_date:
                        message += f"📅 {event_date.text.strip()}\n"
                        message += f"🏆 {event_name.text.strip()}\n"
                        message += "───────────────\n"
            else:
                message += "Não há campeonatos agendados no momento.\n"
        
        message += "\nSe precisar de mais algo pode digitar o que deseja do menu novamente ou usar um desses comandos:\n\n"
        message += HELP_MESSAGE
        await update.message.reply_text(message)
    except Exception as e:
        await update.message.reply_text(f"Desculpe, não foi possível obter os campeonatos no momento. Erro: {str(e)}\n\n{MENU_MESSAGE}")

async def proximos_jogos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Busca e exibe informações sobre os próximos jogos da Fúria.
    Utiliza web scraping para obter dados do site HLTV.org ou dados de exemplo.
    """
    try:
        if MODO_DEVELOPMENT:
            dados = carregar_dados_exemplo()
            if dados and "proximos_jogos" in dados:
                message = "⚔️ Próximos Jogos da Fúria:\n\n"
                for jogo in dados["proximos_jogos"]:
                    message += f"📅 {jogo['data']}\n"
                    message += f"⏰ {jogo['horario']}\n"
                    message += f"🏆 {jogo['campeonato']}\n"
                    message += f"⚔️ Fúria vs {jogo['adversario']}\n"
                    message += f"📋 Formato: {jogo['formato']}\n"
                    message += "───────────────\n"
            else:
                message = "Não há jogos agendados no momento.\n"
        else:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get('https://www.hltv.org/matches', headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            message = "⚔️ Próximos Jogos da Fúria:\n\n"
            
            matches = soup.find_all('div', {'class': 'match'})
            if matches:
                for match in matches:
                    teams = match.find_all('div', {'class': 'team'})
                    if len(teams) >= 2:
                        team1 = teams[0].text.strip()
                        team2 = teams[1].text.strip()
                        if 'Fúria' in team1 or 'Fúria' in team2:
                            date = match.find('div', {'class': 'date'})
                            event = match.find('div', {'class': 'event'})
                            
                            if date and event:
                                message += f"📅 {date.text.strip()}\n"
                                message += f"🏆 {event.text.strip()}\n"
                                message += f"⚔️ {team1} vs {team2}\n"
                                message += "───────────────\n"
            else:
                message += "Não há jogos agendados no momento.\n"
        
        message += "\nSe precisar de mais algo pode digitar o que deseja do menu novamente ou usar um desses comandos:\n\n"
        message += HELP_MESSAGE
        await update.message.reply_text(message)
    except Exception as e:
        await update.message.reply_text(f"Desculpe, não foi possível obter os próximos jogos. Erro: {str(e)}\n\n{MENU_MESSAGE}")

async def estatisticas_do_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Busca e exibe estatísticas gerais do time Fúria.
    Utiliza web scraping para obter dados do site HLTV.org ou dados de exemplo.
    """
    try:
        if MODO_DEVELOPMENT:
            dados = carregar_dados_exemplo()
            if dados and "estatisticas_time" in dados:
                stats = dados["estatisticas_time"]
                message = "📊 Estatísticas da Fúria:\n\n"
                message += f"🏅 Ranking Mundial: #{stats['ranking_mundial']}\n\n"
                
                message += "🎮 Últimas Partidas:\n"
                for partida in stats["ultimas_partidas"]:
                    message += f"📅 {partida['data']}\n"
                    message += f"⚔️ Fúria {partida['placar']} {partida['adversario']}\n"
                    for mapa in partida["mapas"]:
                        message += f"🗺️ {mapa['nome']}: {mapa['placar']}\n"
                    message += "───────────────\n"
                
                message += "\n📈 Estatísticas Gerais:\n"
                message += f"✅ Vitórias: {stats['estatisticas_gerais']['vitorias']}\n"
                message += f"❌ Derrotas: {stats['estatisticas_gerais']['derrotas']}\n"
                message += f"📊 Winrate: {stats['estatisticas_gerais']['winrate']}\n"
                message += f"⭐ Mapas Favoritos: {', '.join(stats['estatisticas_gerais']['mapas_favoritos'])}\n"
                message += f"⚠️ Mapas Evitados: {', '.join(stats['estatisticas_gerais']['mapas_evitados'])}\n"
            else:
                message = "Não foi possível obter as estatísticas do time no momento.\n"
        else:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get('https://www.hltv.org/team/8297/furia', headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            message = "📊 Estatísticas da Fúria:\n\n"
            
            ranking = soup.find('div', {'class': 'ranking'})
            if ranking:
                message += f"🏅 Ranking Mundial: {ranking.text.strip()}\n\n"
            
            message += "🎮 Últimas Partidas:\n"
            matches = soup.find_all('div', {'class': 'match'})
            if matches:
                for match in matches[:5]:
                    teams = match.find_all('div', {'class': 'team'})
                    if len(teams) >= 2:
                        team1 = teams[0].text.strip()
                        team2 = teams[1].text.strip()
                        score = match.find('div', {'class': 'score'})
                        if score:
                            message += f"⚔️ {team1} {score.text.strip()} {team2}\n"
                            message += "───────────────\n"
            else:
                message += "Não há partidas recentes disponíveis.\n"
        
        message += "\nSe precisar de mais algo pode digitar o que deseja do menu novamente ou usar um desses comandos:\n\n"
        message += HELP_MESSAGE
        await update.message.reply_text(message)
    except Exception as e:
        await update.message.reply_text(f"Desculpe, não foi possível obter as estatísticas do time. Erro: {str(e)}\n\n{MENU_MESSAGE}")

async def estatisticas_do_jogador(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Busca e exibe estatísticas individuais dos jogadores da Fúria.
    Utiliza web scraping para obter dados do site HLTV.org ou dados de exemplo.
    """
    try:
        if MODO_DEVELOPMENT:
            dados = carregar_dados_exemplo()
            if dados and "jogadores" in dados:
                message = "👥 Estatísticas dos Jogadores da Fúria:\n\n"
                for nome, stats in dados["jogadores"].items():
                    message += f"🎮 {nome}:\n"
                    message += f"⭐ Rating: {stats['rating']}\n"
                    message += f"🎯 K/D: {stats['kd']}\n"
                    message += f"💥 ADR: {stats['adr']}\n"
                    message += f"🎯 KAST: {stats['kast']}\n"
                    message += f"🔫 Headshot: {stats['headshot']}\n"
                    
                    message += "\n📊 Últimas Partidas:\n"
                    for partida in stats["ultimas_partidas"]:
                        message += f"⭐ Rating: {partida['rating']}\n"
                        message += f"🎯 K/D: {partida['kd']}\n"
                        message += f"💥 ADR: {partida['adr']}\n"
                        message += "───────────────\n"
                    message += "\n"
            else:
                message = "Não foi possível obter as estatísticas dos jogadores no momento.\n"
        else:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            jogadores_furia = {
                'KSCERATO': 'https://www.hltv.org/player/8520/kscerato',
                'arT': 'https://www.hltv.org/player/8519/art',
                'yuurih': 'https://www.hltv.org/player/8521/yuurih',
                'chelo': 'https://www.hltv.org/player/8522/chelo',
                'FalleN': 'https://www.hltv.org/player/921/fallen'
            }
            message = "👥 Estatísticas dos Jogadores da Fúria:\n\n"
            encontrou = False
            for jogador, url in jogadores_furia.items():
                response = requests.get(url, headers=headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                rating = soup.find(string="Rating 2.0")
                kd = soup.find(string="K/D Ratio")
                message += f"🎮 {jogador}: {url}\n"
                if rating or kd:
                    encontrou = True
                    if rating:
                        valor_rating = rating.find_next('span').text if rating.find_next('span') else 'N/A'
                        message += f"⭐ Rating: {valor_rating}\n"
                    if kd:
                        valor_kd = kd.find_next('span').text if kd.find_next('span') else 'N/A'
                        message += f"🎯 K/D: {valor_kd}\n"
                message += "\n"
            if not encontrou:
                message += "Não foi possível encontrar estatísticas detalhadas dos jogadores no momento, mas você pode acessar o perfil de cada um pelo link acima.\n"
        
        message += "\nSe precisar de mais algo pode digitar o que deseja do menu novamente ou usar um desses comandos:\n\n"
        message += HELP_MESSAGE
        await update.message.reply_text(message)
    except Exception as e:
        await update.message.reply_text(f"Desculpe, não foi possível obter as estatísticas dos jogadores. Erro: {str(e)}\n\n{MENU_MESSAGE}")

async def loja(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "🛍️ Loja Oficial da Fúria:\n\n"
        "Confira nossos produtos exclusivos:\n"
        "🔗 https://furia.gg/loja\n\n"
        "Camisetas, moletons, bonés e muito mais com o logo oficial da Fúria!\n\n"
        "Se precisar de mais algo pode digitar o que deseja do menu novamente ou usar um desses comandos:\n\n"
        f"{HELP_MESSAGE}\n"
    )
    await update.message.reply_text(message)

async def redes_sociais(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "📱 Redes Sociais da Fúria:\n\n"
        "Instagram: https://www.instagram.com/furiagg/\n"
        "Twitter: https://twitter.com/furiagg\n"
        "Facebook: https://www.facebook.com/furiagg\n"
        "YouTube: https://www.youtube.com/furiagg\n"
        "TikTok: https://www.tiktok.com/@furiagg\n\n"
        "Siga a Fúria para ficar por dentro de tudo!\n\n"
        "Se precisar de mais algo pode digitar o que deseja do menu novamente ou usar um desses comandos:\n\n"
        f"{HELP_MESSAGE}\n"
    )
    await update.message.reply_text(message)

async def help_comand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Comandos disponíveis:\n"
        "/start - Iniciar o bot\n"
        "/help - Mostrar esta mensagem de ajuda\n"
        "/menu - Voltar ao menu principal\n\n"
    )

# token
app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

# conversação
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        ASKING_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, pegar_nome)],
        SELECT_OPTIONS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu)]
    },
    fallbacks=[]
)

# Adicionando os handlers
app.add_handler(conv_handler)
app.add_handler(CommandHandler('help', help_comand))
app.add_handler(CommandHandler('menu', handle_menu))

# Rodando o bot
app.run_polling()
