import requests
import os

from utils import save_to_file_url, get_file_name


def request(url, file_path='./html/', postfix='html'):
    # Check if file exits
    file_name = get_file_name(url, postfix)
    if os.path.exists(file_path + file_name):
        print("File %s exits, download skipped..."%file_name)
        return

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    r = requests.get(url, headers=headers)

    if file_path:
        save_to_file_url(url, r, file_path, postfix)


