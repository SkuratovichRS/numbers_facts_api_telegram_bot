import configparser

from bot import RunBot

config = configparser.ConfigParser()
config.read('token.ini')
TOKEN = config['TOKEN']['TOKEN']

RunBot(TOKEN)
