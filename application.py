from flask import Flask, request, render_template, redirect
import json, os
from functions import *

app = Flask(__name__)

posts = get_posts()
bookmarks = get_bookmarks()

@app.route("/")
def index():
    return render_template("index.html", posts=posts, bookmarks_counter=len(bookmarks))

@app.route("/post/<id>")
def post_info(id):  # add NO POST exception
    post = posts[int(id) - 1]
    post['views_count'] += 1
    return render_template("post.html", post=post)

@app.route("/search/")
def search_posts():
    s = request.args.get("s")
    # print(s)
    result = []
    if s:
        s = s.lower().strip()
        for post in posts:
            if s in post['content'].lower():
                result.append(post)
            if len(result) == 10:
                break
    return render_template("search.html", posts=result, posts_number=len(result))


@app.route("/users/<user>")
def search_user(user):
    result = [x for x in posts if x['poster_name'] == user]
    return render_template("user-feed.html", posts=result, user_name=user)

@app.route("/tag/<tag>")
def search_tags(tag):
    result = [x for x in posts if '#'+tag in x['tags']]
    return render_template("tag.html", posts=result, tag=tag)

@app.route("/bookmark/<postid>")
def bookmark(postid):
    # проверяем, есть ли пост в закладках
    for post in bookmarks:
        if int(postid) == post['pk']:
            return redirect(f"/bookmarks/remove/{postid}")  # нужно добавить пост в закладки
    return redirect(f"/bookmarks/add/{postid}")  # нужно удалить пост из закладок

@app.route("/bookmarks/add/<postid>")
def bookmark_add(postid):
    for post in posts:
        if int(postid) == post['pk']:
            bookmarks.append(post)
            add_to_bookmarks(post)
            print("added ", post)
            return redirect("/", code=302)
    return redirect("/", code=302)

@app.route("/bookmarks/remove/<postid>")
def bookmark_del(postid):
    print("test ", postid)
    for i in range(len(bookmarks)):
        if int(postid) == bookmarks[i]['pk']:
            print("b ", bookmarks[i]['pk'])
            del bookmarks[i]
            remove_from_bookmarks(postid)
            # print("removed ", posts[i])
            return redirect("/", code=302)
    return redirect("/", code=302)

@app.route("/bookmarks")
def bookmarks_view():
    return render_template("bookmarks.html", posts=bookmarks)

@app.route("/comment_add/<postid>", methods=["POST"])
def comment_add(postid):
    print("id ", postid)
    for i in range(len(posts)):
        if int(postid) == posts[i]['pk']:
            # print("adding comment")
            name = request.form.get("name")
            content = request.form.get("content")
            print(name, content)
            add_comment(postid, name, content)
            posts[i]['comments'] = refresh_comments(int(postid))
            posts[i]['comments_counter'] = len(posts[i]['comments'])
            return redirect(f"/post/{postid}")

if __name__ == '__main__':
    app.run()
