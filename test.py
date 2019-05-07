import os
from flask import Flask, session

app = Flask("app")
app.secret_key = os.urandom(100)


@app.route('/')
def main():
    if "visits" in session:
        session["visits"] = session.get("visits") + 1
    else:
        session["visits"] = 1

    return f"Your visits: {session.get('visits')}"


app.run(host="0.0.0.0", port="99")
