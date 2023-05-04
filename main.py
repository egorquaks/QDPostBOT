import configparser
import telebot

from moviepy.editor import *


def create_config():
    config_file = 'config.ini'
    if not os.path.isfile(config_file):
        config = configparser.ConfigParser()
        config['Settings'] = {
            'bot_token': '',
            'url': ''
        }
        with open(config_file, 'w') as configfile:
            config.write(configfile)
def main():
    create_config()
    config = configparser.ConfigParser()
    config.read('config.ini')
    bot = telebot.TeleBot(config.get('Settings', 'bot_token'))

    @bot.message_handler(commands=['help', 'start'])
    def get_text_messages(message):
        bot.send_message(message.from_user.id, "Пришли мне изображение которое ты хотел бы обработать")

    bot.infinity_polling()


if __name__ == '__main__':
    main()
