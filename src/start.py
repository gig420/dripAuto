import os
import threading
import logging
import getpass
import cryptocode

try:
    import coloredlogs
except ImportError:
    coloredlogs = None

import src.constants as con

from src.drip import Drip
from src.config import Config

from argparse import ArgumentParser
from logging.handlers import TimedRotatingFileHandler
from cryptography.fernet import Fernet

class Start:
    def __init__(self):
        config = Config()

        threading.current_thread().name = "Core"

        parser = ArgumentParser(description=con.DESCRIPTION)
        parser.add_argument('-encrypt', dest='encrypt', action='store_true', help='Encrypt your privatekey')
        parser.add_argument("-nolog", dest="savelog", action="store_false", help="don't save log-files", required=False, default=True)
        parser.add_argument("-log", dest="loglevel", type=int, choices=[10, 20, 30, 40, 50], help="debug, info, warning, error, critical", default=30, required=False)
        args = parser.parse_args()

        logger = logging.getLogger()
        logger.setLevel(args.loglevel)

        log_file = os.path.join(con.DIR_LOG, con.FILE_LOG)
        log_format = config.get('MAIN', 'LOG_FORMAT')

        if coloredlogs:
            coloredlogs.install(logger=logger, fmt=log_format, level=args.loglevel, datefmt='%H:%M:%S')
        else:
            console_log = logging.StreamHandler()
            console_log.setFormatter(logging.Formatter(log_format))
            console_log.setLevel(self.args.loglevel)
            logging.basicConfig(format=log_format, level=self.args.loglevel)

        if args.savelog:
            log_path = os.path.dirname(log_file)
            if not os.path.exists(log_path):
                os.makedirs(log_path)
            file_log = TimedRotatingFileHandler(log_file, when="d", encoding="utf-8")
            file_log.setFormatter(logging.Formatter(log_format))
            file_log.setLevel(args.loglevel)
            logger.addHandler(file_log)

        ascii_art = os.path.join(con.DIR_RES, con.ASCII_ART)
        with open(ascii_art, "r", encoding="utf8") as file:
            content = file.readlines()
        text = "".join(content)
        print(f' {text} ')
        print(f'{con.DESCRIPTION} ({con.VERSION})\n')

        config_file_path = os.path.join(con.DIR_CFG, con.FILE_CFG)

        if not os.path.isfile(config_file_path):
            logging.info(f'{config_file_path} does not exist.')

            # Copy the template file to the config file if there is no config file.
            with open(os.path.join(con.DIR_CFG, con.FILE_TMPCFG), encoding="utf8") as template_cfg_file, \
                    open(config_file_path, "w", encoding="utf8") as user_cfg_file:
                user_cfg_file.write(template_cfg_file.read())

            logging.fatal("A config file has been created."
                        " Customize it, then restart the script!")
            exit(1)

        if config.get('MAIN', 'SECURE_KEY'):
            password = getpass.getpass("Enter your password: \n")
            decrypted_password = cryptocode.decrypt(config.get('MAIN', 'SECURE_KEY'), password)
            if decrypted_password:
                logging.info('Authentication successful.')
                if args.encrypt:
                    pk_input = input("Please enter your private-key you want to encrypt: ")
                    encrypted_pk = Fernet(decrypted_password).encrypt(pk_input.encode()).decode('utf-8')
                    print(f'Encrypted private key: {encrypted_pk}')
                else:
                    Drip(decrypted_password)

            elif not password:
                logging.fatal('No password provided.')
            else:
                logging.fatal('Incorrect password.')
        else:
            new_password = getpass.getpass()
            key = Fernet.generate_key().decode()
            encrypted_password = cryptocode.encrypt(key, new_password).encode().decode()
            config.set('MAIN', 'SECURE_KEY', encrypted_password)
            logging.info('SECURE_KEY not set, new key generated and password saved.')
            if args.encrypt:
                pk_input = input("Please enter your private-key you want to encrypt: ")
                encrypted_pk = Fernet(decrypted_password).encrypt(pk_input.encode()).decode('utf-8')
                print(f'Encrypted private key: {encrypted_pk}')
