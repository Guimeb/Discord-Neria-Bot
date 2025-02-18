import logging

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,  # Define o nível de log (INFO, DEBUG, ERROR)
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),  # Salva logs em um arquivo
        logging.StreamHandler()  # Exibe logs no terminal
    ]
)

# Criar um logger
logger = logging.getLogger("discord_bot")
