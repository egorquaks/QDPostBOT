import os
import configparser
def createConfig():
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
    createConfig()
if __name__ == '__main__':
    main()
