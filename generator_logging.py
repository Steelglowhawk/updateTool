import logging
import pathlib


def log_event(message):
	log_dir_name = 'logs'
	log_file_name = 'log.log'
	pathlib.Path.cwd().joinpath(log_dir_name).mkdir(exist_ok=True)
	log_dir_path = pathlib.Path.cwd().joinpath(log_dir_name)
	log_file_path = pathlib.Path(log_dir_path).joinpath(log_file_name)
	logging.disable(logging.DEBUG)
	logging.basicConfig(filename=log_file_path, level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
	logging.basicConfig(filename=log_file_path, level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')
	logging.info(message)


if __name__ == '__main__':
	log_event('Alarm 001')
