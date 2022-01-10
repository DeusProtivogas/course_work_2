import json
import os

DATA_FOLDER = os.path.dirname(os.path.realpath(__file__)) + "\\data"


def get_posts():
    """
    Получение списка постов с комментариями
    :return: список словарей постов с комментариями
    """
    # with open('data/data.json', 'r', encoding='UTF-8') as f:  # для heroku
    with open(os.path.join(DATA_FOLDER, 'data.json'), 'r', encoding='UTF-8') as f:  # для тестирования на машине
        raw_json = f.read()
    posts = json.loads(raw_json)
    comments = get_comments()
    for post in posts:
        post['comments'] = [x for x in comments if
                            x['post_id'] == post['pk']]  # добавление комментариев напрямую в пост
        post['comments_counter'] = len(post['comments'])
        post['conjugate'] = conjugate_comment(post['comments_counter'])  # правильная форма слова "комментарий"
        post['content_short'] = post['content'][:47].strip("., !?") + "..."  # короткий текст, оканчивается на "..."
        post['tags'] = get_tags(post)  # получение тегов поста
        for tag in post['tags']:
            # обрамление тегов в ссылки в полном и кратком содержании
            post['content'] = post['content'].replace(" " + tag + " ", " " + tag_to_link(tag) + " ")
            post['content_short'] = post['content_short'].replace(" " + tag + " ", " " + tag_to_link(tag) + " ")
    return posts


def get_comments():
    """
    Получение количества комментариев
    :return: кол-во комментариев
    """
    # with open('data/comments.json', 'r', encoding='UTF-8') as f:  # для heroku
    with open(os.path.join(DATA_FOLDER, 'comments.json'), 'r', encoding='UTF-8') as f:  # для тестирования на машине
        raw_json = f.read()
    comments = json.loads(raw_json)
    return comments


def conjugate_comment(num):
    """
    Выбрать правильное склонение слова "комментарий" в зависимости от количества
    :param num: количество комментариев
    :return: склонение слова "комментарий"
    """
    if num % 10 == 1 or (12 <= num % 100 <= 19):
        return "комментарий"
    if 2 <= num % 10 <= 4:
        return "комментария"
    return "комментариев"


def get_tags(post):
    """
    получение всех тегов в посте
    :param post: пост, в тексте которого ищем теги
    :return: сортированный список тегов поста без повторений
    """
    tags = [x for x in post['content'].split(" ") if x.startswith("#")]
    return sorted(list(set(tags)))


def tag_to_link(tag):
    """
    Обрамление тега в ссылку для шаблона
    :param tag: тег
    :return: строка, которая станет ссылкой в шаблоне
    """
    return f'<a href="/tag/{tag[1:]}">{tag}</a>'


def get_bookmarks():
    """
    получение постов в закладках
    :return: список постов, помещенных в закладки
    """
    # with open('data/bookmarks.json', 'r', encoding='UTF-8') as f:  # для heroku
    with open(os.path.join(DATA_FOLDER, 'bookmarks.json'), 'r', encoding='UTF-8') as f:  # для тестирования на машине
        raw_json = f.read()
    posts = json.loads(raw_json)
    return posts


def add_to_bookmarks(post):
    """
    запись поста в файл закладок
    :param post: пост, который нужно добавить в закладки
    """
    # with open('data/bookmarks.json', 'r', encoding='UTF-8') as f:  # для heroku
    with open(os.path.join(DATA_FOLDER, 'bookmarks.json'), 'r', encoding='UTF-8') as f:  # для тестирования на машине
        raw_json = f.read()
    posts = json.loads(raw_json)
    posts.append(post)

    raw_json = json.dumps(posts)
    # with open('data/bookmarks.json', 'w', encoding='UTF-8') as f:  # для heroku
    with open(os.path.join(DATA_FOLDER, 'bookmarks.json'), 'w', encoding='UTF-8') as f:  # для тестирования на машине
        f.write(raw_json)


def remove_from_bookmarks(postid):
    """
    удаление поста из файла закладок
    :param postid: id поста, который нужно удалить
    """
    # with open('data/bookmarks.json', 'r', encoding='UTF-8') as f:  # для heroku
    with open(os.path.join(DATA_FOLDER, 'bookmarks.json'), 'r', encoding='UTF-8') as f:  # для тестирования на машине
        raw_json = f.read()
    posts = json.loads(raw_json)
    for i in range(len(posts)):
        if int(postid) == int(posts[i]['pk']):
            del posts[i]
            break

    raw_json = json.dumps(posts)
    # with open('data/bookmarks.json', 'w', encoding='UTF-8') as f:  # для heroku
    with open(os.path.join(DATA_FOLDER, 'bookmarks.json'), 'w', encoding='UTF-8') as f:  # для тестирования на машине
        f.write(raw_json)


def add_comment(postid, name, content):
    """
    добавление комментария к посту
    :param postid: id поста, в который записываем комментарий
    :param name: имя пользователя, оставившего комментарий
    :param content: содержание поста
    :return:
    """
    comments = get_comments()
    comment_id = max([i['pk'] for i in comments])  # получение нового id комментария (максимальный id из доступных + 1)
    comment = {  # создание нового комментария
        'post_id': int(postid),
        'commenter_name': name,
        'comment': content,
        'pk': comment_id + 1,
    }
    comments.append(comment)  # запись комментария

    raw_json = json.dumps(comments)
    # with open('data/comments.json', 'w', encoding='UTF-8') as f:  # для heroku
    with open(os.path.join(DATA_FOLDER, 'comments.json'), 'w', encoding='UTF-8') as f:  # для тестирования на машине
        f.write(raw_json)


def refresh_comments(postid):
    """
    обновление комментариев у поста
    :param postid: id поста
    :return: новый список комментариев к посту
    """
    comments = get_comments()
    return [x for x in comments if x['post_id'] == postid]
