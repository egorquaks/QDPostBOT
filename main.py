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
        sys.exit()


def main():
    create_config()
    config = configparser.ConfigParser()
    config.read('config.ini')
    bot = telebot.TeleBot(config.get('Settings', 'bot_token'))

    @bot.message_handler(commands=['help', 'start'])
    def get_text_messages(message):
        bot.send_message(message.from_user.id, "Пришли мне изображение которое ты хотел бы обработать")

    @bot.message_handler(content_types=['document'])
    def handle_gif(message):
        if message.document.mime_type == "image/gif":
            bot.reply_to(message, "Обрабатываю...")
            file_info = bot.get_file(message.document.file_id).file_path
            file = bot.download_file(file_info)
            with open("temp.gif", 'wb') as f:
                f.write(file)
            bot.reply_to(message, "Гиф успешно сохранена, приступаю к обработке!")

    @bot.message_handler(content_types=['animation'])
    def handle_animation(message):
        bot.reply_to(message, "Обрабатываю...")
        file_info = bot.get_file(message.document.file_id).file_path
        file = bot.download_file(file_info)
        with open("temp.mp4", 'wb') as f:
            f.write(file)
        clip = VideoFileClip('temp.mp4')
        clip.write_gif('temp.gif')
        bot.reply_to(message, "Гиф успешно сохранена, приступаю к обработке!")

    bot.infinity_polling()


if __name__ == '__main__':
    main()
