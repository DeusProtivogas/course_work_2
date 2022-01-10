import json
import os

DATA_FOLDER = os.path.dirname(os.path.realpath(__file__)) + "\\data"


# DATA_FOLDER = "data"


# "data/data.json"
# print(DATA_FOLDER)
# os.path.join(UPLOAD_FOLDER, 'filename.png')
def get_posts():
    """
    Получение списка постов с комментариями
    :return: список словарей постов с комментариями
    """
    # with open('data\\data.json', 'r', encoding='UTF-8') as f:
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
        # print(post['content'])
        post['content_short'] = post['content'][:47].strip("., !?") + "..."
        post['tags'] = get_tags(post)
        for tag in post['tags']:
            post['content'] = post['content'].replace(" " + tag + " ", " " + tag_to_link(tag) + " ")
            # print(post['content'])
            post['content_short'] = post['content_short'].replace(" " + tag + " ", " " + tag_to_link(tag) + " ")
        # print(post['content'])

        # post['content_very_short'] = post['content'][:7].strip("., !?") + "..."
    #     print(post)
    # print(posts)
    return posts


def get_comments():
    """
    Получение количества комментариев
    :return: кол-во комментариев
    """
    # with open('data\\comments.json', 'r', encoding='UTF-8') as f:
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


def get_tags(post):
    tags = [x for x in post['content'].split(" ") if x.startswith("#")]
    # print(tags)
    return sorted(list(set(tags)))


def tag_to_link(tag):
    return f'<a href="/tag/{tag[1:]}">{tag}</a>'

def get_bookmarks():
    # with open('data/bookmarks.json', 'r', encoding='UTF-8') as f:
    with open(os.path.join(DATA_FOLDER, 'bookmarks.json'), 'r', encoding='UTF-8') as f:
        raw_json = f.read()
    posts = json.loads(raw_json)
    return posts

def add_to_bookmarks(post):
    # with open('data/bookmarks.json', 'r', encoding='UTF-8') as f:
    with open(os.path.join(DATA_FOLDER, 'bookmarks.json'), 'r', encoding='UTF-8') as f:
        raw_json = f.read()
        # print(raw_json)
    posts = json.loads(raw_json)
    posts.append(post)

    raw_json = json.dumps(posts)
    # with open('data/bookmarks.json', 'w', encoding='UTF-8') as f:
    with open(os.path.join(DATA_FOLDER, 'bookmarks.json'), 'w', encoding='UTF-8') as f:
        f.write(raw_json)


def remove_from_bookmarks(postid):
    # with open('data/bookmarks.json', 'r', encoding='UTF-8') as f:
    with open(os.path.join(DATA_FOLDER, 'bookmarks.json'), 'r', encoding='UTF-8') as f:
        raw_json = f.read()
        # print(raw_json)
    posts = json.loads(raw_json)
    # posts.append(post)
    # posts = [x for x in posts if not (post['pk'] == x['pk'])]
    print(postid)
    for i in range(len(posts)):
        # print(posts[i])
        if int(postid) == int(posts[i]['pk']):
            print("testing")
            del posts[i]
            break

    raw_json = json.dumps(posts)
    # with open('data/bookmarks.json', 'w', encoding='UTF-8') as f:
    with open(os.path.join(DATA_FOLDER, 'bookmarks.json'), 'w', encoding='UTF-8') as f:
        f.write(raw_json)


def add_comment(postid, name, content):
    comments = get_comments()
    comment_id = max([i['pk'] for i in comments])
    print(comment_id)
    comment = {
        'post_id': int(postid),
        'commenter_name': name,
        'comment': content,
        'pk': comment_id + 1,
    }
    comments.append(comment)

    raw_json = json.dumps(comments)
    # with open('data/comments.json', 'w', encoding='UTF-8') as f:
    with open(os.path.join(DATA_FOLDER, 'comments.json'), 'w', encoding='UTF-8') as f:
        f.write(raw_json)

def refresh_comments(postid):
    comments = get_comments()
    return [x for x in comments if x['post_id'] == postid]

# get_posts()