import json
import os

DATA_FOLDER = os.path.dirname(os.path.realpath(__file__)) + "\\data"


# DATA_FOLDER = "data"


# "data/data.json"
# os.path.join(DATA_FOLDER,
# print(DATA_FOLDER)
# os.path.join(UPLOAD_FOLDER, 'filename.png')
def get_posts():
    """
    Получение списка постов с комментариями
    :return: список словарей постов с комментариями
    """
    # with open('data/data.json', 'r', encoding='UTF-8') as f:
    with open(os.path.join(DATA_FOLDER, 'data.json'), 'r', encoding='UTF-8') as f:
        raw_json = f.read()
        # print(raw_json)
    posts = json.loads(raw_json)
    comments = get_comments()
    for post in posts:
        post['comments'] = [x for x in comments if x['post_id'] == post['pk']]
        post['comments_counter'] = len(post['comments'])
        post['conjugate'] = conjugate_comment(post['comments_counter'])
        post['content_short'] = post['content'][:47].strip("., !?") + "..."
        # post['content_very_short'] = post['content'][:7].strip("., !?") + "..."
    #     print(post)
    # print(posts)
    return posts


def get_comments():
    """
    Получение количества комментариев
    :return: кол-во комментариев
    """
    # with open('data/comments.json', 'r', encoding='UTF-8') as f:
    with open(os.path.join(DATA_FOLDER, 'comments.json'), 'r', encoding='UTF-8') as f:
        raw_json = f.read()
        # print(raw_json)
    comments = json.loads(raw_json)
    return comments


def conjugate_comment(num):
    """
    Выбрать правильное склонение слова "комментарий" в зависимости от количества
    :param num: количество комментариев
    :return: склонение слова "комментарий"
    """
    if num % 10 == 1:
        return "комментарий"
    if 2 <= num % 10 <= 4:
        return "комментария"
    return "комментариев"


# get_posts()
