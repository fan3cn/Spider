import os


def save_to_file_url(url, r, file_path, postfix):
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    file_name = get_file_name(url, postfix)

    with open(file_path + file_name, 'wb+') as f:
        f.write(r.content)


def save_to_file(path, file_name, content, once=False):
    if not os.path.exists(path):
        os.makedirs(path)

    path = path + file_name

    if os.path.exists(path) and once:
        return

    #print(content)

    with open(path, 'w+') as f:
        f.write(content)


def save_to_file_append(path, file_name, content):
    if not os.path.exists(path):
        os.makedirs(path)

    path = path + file_name

    # if os.path.exists(path):
    #     return

    with open(path, 'a+') as f:
        f.write(content)


def get_file_name(url, postfix='html'):
    file_name = url.split("/")[-1]

    if file_name == 'review_all':
        file_name = url.split("/")[-2] + '_' + file_name

    if '.' not in file_name:
        file_name = file_name + '.' + postfix
    return file_name