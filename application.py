from flask import Flask, request, render_template, redirect
from functions import *

app = Flask(__name__)

posts = get_posts()  # Получить все посты и комментарии
bookmarks = get_bookmarks()  # Получить все закладки


@app.route("/")
def index():  # главная страница
    return render_template("index.html", posts=posts, bookmarks_counter=len(bookmarks))


@app.route("/post/<id>")
def post_info(id):  # вывести информацию о посте
    for post in posts:  # проверка на существование поста
        if int(id) == post['pk']:
            post = posts[int(id) - 1]
            post['views_count'] += 1
            return render_template("post.html", post=post)
    return redirect("/", code=302)  # если поста нет, вернуться на главную страницу


@app.route("/search/")  # поиск по последовательности букв
def search_posts():
    s = request.args.get("s")  # получаем аргумент
    result = []
    if s:  # проверка на пустой аргумент
        s = s.lower().strip()  # поиск не зависит от регистра
        for post in posts:
            if s in post['content'].lower():
                result.append(post)
            if len(result) == 10:  # выводим максимум 10 постов
                break
    return render_template("search.html", posts=result, posts_number=len(result))


@app.route("/users/<user>")
def search_user(user):  # посты пользователя
    result = [x for x in posts if x['poster_name'] == user]  # поиск постов
    return render_template("user-feed.html", posts=result, user_name=user)


@app.route("/tag/<tag>")
def search_tags(tag):  # посты по тэгу
    result = [x for x in posts if '#' + tag in x['tags']]  # поиск тега среди тегов поста
    return render_template("tag.html", posts=result, tag=tag)


@app.route("/bookmark/<postid>")
def bookmark(postid):
    # проверяем, есть ли пост в закладках (сделано, чтобы нажатие на флажок могло и добавлять в закладки,
    # и удалять из закладок)
    for post in bookmarks:
        if int(postid) == post['pk']:
            return redirect(f"/bookmarks/remove/{postid}")  # нужно добавить пост в закладки
    return redirect(f"/bookmarks/add/{postid}")  # нужно удалить пост из закладок


@app.route("/bookmarks/add/<postid>")  # добавляем пост в закладки
def bookmark_add(postid):
    for post in posts:  # проверка на существование поста
        if int(postid) == post['pk']:
            bookmarks.append(post)  # добавляем пост в список закладок
            add_to_bookmarks(post)  # записываем пост в файл закладок
            return redirect("/", code=302)
    return redirect("/", code=302)  # если пост не существует, возвращаемся на главную страницу


@app.route("/bookmarks/remove/<postid>")  # удаляем пост из закладок
def bookmark_del(postid):
    for i in range(len(bookmarks)):  # проверка на существование файла в закладках
        if int(postid) == bookmarks[i]['pk']:
            del bookmarks[i]
            remove_from_bookmarks(postid)
            return redirect("/", code=302)
    return redirect("/", code=302)


@app.route("/bookmarks")  # вывести все закладки
def bookmarks_view():
    return render_template("bookmarks.html", posts=bookmarks)


@app.route("/comment_add/<postid>", methods=["POST"])  # добавление комментария к посту
def comment_add(postid):
    for i in range(len(posts)):
        if int(postid) == posts[i]['pk']:
            name = request.form.get("name")  # получение имени и контента из формы
            content = request.form.get("content")
            add_comment(postid, name, content)  # запись комментария в файл
            posts[i]['comments'] = refresh_comments(int(postid))  # добавление комментария в список комментариев поста
            posts[i]['comments_counter'] = len(posts[i]['comments'])  # обновление счетчика комментариев
            return redirect(f"/post/{postid}")


if __name__ == '__main__':
    app.run()
