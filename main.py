import configparser
import telebot
from PIL import Image, ImageSequence

from moviepy.editor import *


def create_frame_array(gif_path):
    frames = []

    with Image.open(gif_path) as im:
        # Итерируемся по всем кадрам GIF-анимации
        for frame in range(0, im.n_frames):
            im.seek(frame)  # Переходим к текущему кадру
            frame_data = im.copy()  # Создаем копию кадра
            frames.append(frame_data)  # Добавляем кадр в массив

    return frames


def convert_to_gif(video_path, gif_path):
    clip = VideoFileClip(video_path)
    duration_per_frame = 1 / clip.fps  # Рассчитываем длительность каждого кадра

    frames = []
    for frame in clip.iter_frames():
        img = Image.fromarray(frame)
        frames.append(img)

    # Сохраняем GIF-анимацию с использованием исходной частоты кадров
    frames[0].save(gif_path, save_all=True, append_images=frames[1:], loop=0, duration=duration_per_frame * 1000)


def crop_image(image_path, target_size):
    with Image.open(image_path) as im:
        # Определяем размер исходного изображения
        original_width, original_height = im.size

        # Вычисляем границы для обрезки изображения
        target_width, target_height = target_size
        left = (original_width - target_width) // 2
        top = (original_height - target_height) // 2
        right = left + target_width
        bottom = top + target_height

        # Обрезаем изображение
        cropped_image = im.crop((left, top, right, bottom))

    return cropped_image


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


def resize():
    with Image.open('temp.gif') as im:
        # Изменяем размер исходной гиф-анимации, чтобы ширина была равна 1856
        wpercent = (1856 / float(im.size[0]))
        hsize = int((float(im.size[1]) * float(wpercent)))
        source_frames = create_frame_array('temp.gif')
        frames_resized = []
        for frame in source_frames:
            frame1 = frame.resize((1856, hsize))
            frames_resized.append(frame1)
        # Создаем новую гиф-анимацию с заданными параметрами
        frames = []
        duration = []
        text = Image.open('showcase solo.png')
        logo = Image.open('logos.png')
        for frame in frames_resized:
            # new_frame = Image.new('RGBA', (1920, hsize + 396), (0, 0, 0, 0))
            new_frame = crop_image('background.png', (1920, hsize + 396))
            new_frame.paste(frame, ((1920 - frame.width) // 2, 354))
            new_frame.paste(text, (0, 0), text)
            new_frame.paste(logo, (0, 0), logo)
            frames.append(new_frame)
            duration.append(frame.info['duration'])

        # Сохраняем новую гиф-анимацию
        frames[0].save('new.gif', save_all=True, append_images=frames[1:], loop=0, duration=duration, optimize=True)


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
            bot.reply_to(message, "Загружаю...")
            file_info = bot.get_file(message.document.file_id).file_path
            file = bot.download_file(file_info)
            with open("temp.gif", 'wb') as f:
                f.write(file)
            bot.reply_to(message, "Гиф успешно сохранена! Обрабатываю")
            resize()
            bot.reply_to(message, "Обработано")
            f = open("new.gif", "rb")
            bot.send_document(message.chat.id, f)

    @bot.message_handler(content_types=['animation'])
    def handle_animation(message):
        bot.reply_to(message, "Загружаю...")
        file_info = bot.get_file(message.document.file_id).file_path
        file = bot.download_file(file_info)
        with open("temp.mp4", 'wb') as f:
            f.write(file)
        convert_to_gif('temp.mp4', 'temp.gif')
        bot.reply_to(message, "Гиф успешно сохранена! Обрабатываю")
        resize()
        bot.reply_to(message, "Обработано")
        f = open("new.gif", "rb")
        bot.send_document(message.chat.id, f)

    bot.infinity_polling()


if __name__ == '__main__':
    main()
