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
def post_info(id):
    post = posts[int(id) - 1]
    post['views_count'] += 1
    return render_template("post.html", post=post)


if __name__ == '__main__':
    app.run(debug=True)
