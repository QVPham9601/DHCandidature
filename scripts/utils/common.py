import os

import requests

from utils.logger import get_logger

logger = get_logger(__name__)


def mkdir_p(path):
    if not (os.path.exists(path)):
        logger.info('Creating %s' % path)
        os.mkdir(path)


def remove_if_exist(path):
    if os.path.exists(path):
        logger.debug('Deleting %s' % path)
        os.remove(path)


def download_file(url, filename):
    '''
        Usage: download(url, filename)
        This function downloads content from url link and save it under 'filename'
        Params(2):
            url:        the URL link
            filename:       The filename to be saved.
    '''
    r = requests.get(url)
    with open(filename, "wb") as fo:
        fo.write(r.content)
    return filename
