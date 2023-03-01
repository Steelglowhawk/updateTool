import logging
import pathlib


log_path = pathlib.Path.cwd().joinpath('log')
logging.basicConfig(filename=log_path, level=logging.DEBUG, format=' %(asctime)s - %(leveltime)s - %(message)s')
logging.debug('Start of program')