import logging
from json import load
from os.path import isdir
from time import time

import pandas as pd

if __name__ == '__main__':
    start_time = time()

    formatter = logging.Formatter('%(asctime)s : %(name)s :: %(levelname)s : %(message)s')
    logger = logging.getLogger('main')
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    console_handler.setLevel(logging.DEBUG)
    logger.debug('started')

    output_folder = '../output/'

    output_folder_exists = isdir(output_folder)
    if not output_folder_exists:
        logger.warning('output folder %s does not exist. Quitting.' % output_folder)
        quit()

    input_folder = '../data/'

    input_folder_exists = isdir(input_folder)
    if not input_folder_exists:
        logger.warning('input folder %s does not exist. Quitting.' % input_folder)
        quit()

    with open('./settings.json') as settings_fp:
        settings = load(settings_fp)
        logger.debug(settings)

    data_frames = dict()
    input_files = None
    key = 'all_input_files'
    if key in settings.keys():
        input_files = settings[key]
    else:
        logger.warning('required key %s is not in the settings. Quitting.' % key)
        quit()
    for item in input_files:
        short_item = item.replace('.txt', '')
        input_file = input_folder + item
        logger.debug('loading data from %s' % input_file)
        data = pd.read_csv(input_file)
        logger.debug(data.shape)
        logger.debug(data.columns.values)
        data_frames[short_item] = data

    logger.debug('done')
    finish_time = time()
    elapsed_hours, elapsed_remainder = divmod(finish_time - start_time, 3600)
    elapsed_minutes, elapsed_seconds = divmod(elapsed_remainder, 60)
    logger.info("Time: {:0>2}:{:0>2}:{:05.2f}".format(int(elapsed_hours), int(elapsed_minutes), elapsed_seconds))
    console_handler.close()
    logger.removeHandler(console_handler)
