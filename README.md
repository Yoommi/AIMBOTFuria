# AIMBot - Bot da Fúria Esports

O AIMBot é um bot do Telegram desenvolvido para fornecer informações sobre a Fúria Esports, incluindo campeonatos, próximos jogos, estatísticas do time e jogadores, produtos da loja oficial e redes sociais.

## 🤖 Acesse o Bot

Você pode acessar o bot de duas maneiras:
1. Clique direto no link: [AIMBot Furia](https://t.me/aimbotfuria_bot)
2. Busque por `@aimbotfuria_bot` no Telegram

## 🚀 Funcionalidades

- 📅 Próximos Campeonatos
- ⚔️ Próximos Jogos
- 📊 Estatísticas do Time
- 👥 Estatísticas dos Jogadores
- 🛍️ Produtos da Loja Oficial
- 📱 Redes Sociais

## 🛠️ Tecnologias Utilizadas

- Python 3.x
- python-telegram-bot
- BeautifulSoup4
- Requests

## 📋 Pré-requisitos

- Python 3.x instalado
- Token do Bot do Telegram
- Bibliotecas Python necessárias

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/aimbot-furia.git
cd aimbot-furia
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure o token do bot:
- Crie um arquivo `.env` na raiz do projeto
- Adicione seu token do bot:
```
TELEGRAM_BOT_TOKEN=seu_token_aqui
```

## 🚀 Como Executar

1. Execute o bot:
```bash
python aimbot.py
```

## 🛠️ Modo de Desenvolvimento

O bot possui um modo de desenvolvimento que utiliza dados de exemplo para demonstração:

1. Por padrão, o bot está configurado para usar dados de exemplo (`MODO_DEVELOPMENT = True`)
2. Para usar dados reais do HLTV.org, altere `MODO_DEVELOPMENT` para `False` no arquivo `aimbot.py`
3. Os dados de exemplo estão no arquivo `dados_exemplo.json`

### Estrutura dos Dados de Exemplo

O arquivo `dados_exemplo.json` contém informações fictícias mas realistas sobre:
- Próximos campeonatos
- Próximos jogos
- Estatísticas do time
- Estatísticas individuais dos jogadores

## 🤖 Comandos Disponíveis

- `/start` - Iniciar o bot
- `/help` - Mostrar mensagem de ajuda
- `/menu` - Voltar ao menu principal

## 📝 Estrutura do Projeto

```
aimbot-furia/
├── aimbot.py              # Arquivo principal do bot
├── dados_exemplo.json     # Dados de exemplo para demonstração
├── nomes.json             # Armazenamento de nomes dos usuários
├── buscar_proximos_jogos.py
├── estatisticas_do_time.py
├── estatisticas_do_jogador.py
├── redes_sociais.py
├── loja.py
└── README.md
```

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📞 Suporte

Para suporte, entre em contato através das issues do GitHub ou envie um e-mail para [seu-email@exemplo.com]. 