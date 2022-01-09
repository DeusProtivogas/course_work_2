from flask import Flask, request, render_template
import json, os
from functions import *

# TEMPLATE_FOLDER = os.path.dirname(os.path.realpath(__file__)) + "\\templates"

app = Flask(__name__)

# print("AAA  ", os.path.join(os.path.dirname(__file__), 'templates'))
posts = get_posts()

@app.route("/")
def index():
    return render_template("index.html", posts=posts)

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
        print(result)
    return render_template("search.html", posts=result, posts_number=len(result))


@app.route("/users/<user>")
def search_user(user):
    print(user)
    result = [x for x in posts if x['poster_name'] == user]
    print(result)
    return render_template("user-feed.html", posts=result, user_name=user)



if __name__ == '__main__':
    app.run(debug=True)
