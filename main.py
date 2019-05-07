from flask import Flask, request, render_template, session
import os
import datetime

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",
          "December"]
accounts = []
posts = [
    {
        "title": "Welcome To Blog!",
        "author": "The Dev Team",
        "date_posted": "The day Blog was released",
        "content": "Welcome to Blog! Have fun!",
        "comments": ["The Dev Team: This is a comment", "The Dev Team: This is another comment."],
        "id": "0"
    }
]


def valid(username, password):
    for account in accounts:
        if account["username"] == username and account["password"] == password:
            return True

    return False


def exists(username, password):
    for account in accounts:
        if account["username"] == username:
            return [True, "Username"]

        elif account["password"] == password:
            return[True, "Password"]

    return [False]


def search(id):
    i = 0
    global posts
    while i < len(posts):
        if int(posts[i]["id"]) == int(id):
            return i

        i += 1
    return "Not Found"


app = Flask(__name__)
app.secret_key = os.urandom(100)


@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == "GET":
        session["username"] = ""
        session["signedin"] = False
        return render_template("home.html", posts=posts, username=session.get("username"),
                               signedin=session.get("signedin"))

    else:
        return "Error 7: Invalid POST argument"


@app.route('/gotologin', methods=["POST", "GET"])
def gotologin():
    if request.method == "POST":
        if request.form["login"] == "Log In":
            return render_template("login.html", message="")

        else:
            return render_template("newaccount.html")


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        if valid(request.form["username"], request.form["password"]):
            session["username"] = request.form["username"]
            session["signedin"] = True
            return render_template("home.html", posts=posts,
                                   username=session.get("username"), signedin=session.get("signedin"))

        else:
            return render_template("login.html", message="A detail was incorrect")


@app.route('/newaccount', methods=["POST", "GET"])
def newaccount():
    if request.method == "POST":
        if not exists(request.form["username"], request.form["password"])[0]:
            accounts.append(
                {
                    "username": request.form["username"],
                    "password": request.form["password"]
                }
            )
            session["signedin"] = True
            session["username"] = request.form["username"]
            return render_template("home.html", posts=posts, username=session.get("username"),
                                   signedin=session.get("signedin"))

        else:
            existsdata = exists(request.form["username"], request.form["password"])
            return render_template("newaccount.html", message=f"{existsdata[1]} Already Exists")


@app.route('/userfunctions', methods=["POST", "GET"])
def userfunctions():
    if request.method == "POST":
        if request.form["button"] == "Create New Post":
            return render_template("newpost.html", message="", username=session.get("username"))

        else:
            session["signedin"] = False
            session["username"] = ""
            return render_template("home.html", posts=posts, username=session.get("username"),
                                   signedin=session.get("signedin"))


@app.route('/newpost', methods=["POST", "GET"])
def newpost():
    if request.method == "POST":
        now = datetime.datetime.now()
        posts.insert(
            0,
            {
                "title": request.form["title"],
                "author": session.get("username"),
                "date_posted": f"{months[now.month - 1]} {now.day}, {now.year}",
                "content": request.form["content"],
                "comments": [],
                "id": len(posts)
            }
        )
        return render_template("home.html", posts=posts, username=session.get("username"),
                               signedin=session.get("signedin"))


@app.route('/comment', methods=["POST", "GET"])
def comment():
    if request.method == "POST":
        if not search(request.form["id"]) == "Not Found":
            posts[search(request.form["id"])]["comments"].append(f"{session.get('username')}: "
                                                                 f"{request.form['comment']}")
            return render_template("home.html", posts=posts, username=session.get("username"),
                                   signedin=session.get("signedin"))

        else:
            return "Error 707: Post Not Found"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8080")
