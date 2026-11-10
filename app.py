import sqlite3

from flask import Flask, render_template, request

app = Flask(__name__)
DATABASE = "database.db"


def setup_database():
    with sqlite3.connect(DATABASE) as db:
        db.execute(
            "CREATE TABLE IF NOT EXISTS users "
            "(username TEXT, password TEXT)"
        )
        if db.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
            db.execute(
                "INSERT INTO users VALUES (?, ?)",
                ("rudolf.servatka", "123"),
            )


@app.route("/", methods=["GET", "POST"])
def login():
    username = ""
    password = ""
    query = ""
    result = ""
    success = False

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        #vstup sucastou
        query = (
            "SELECT * FROM users WHERE username = '"
            + username
            + "' AND password = '"
            + password
            + "'"
        )

        print(
            "SQL príkaz:",
            query,
            f"| parametre: username={username!r}, password={password!r}",
        )

        try:
            with sqlite3.connect(DATABASE) as db:
                user = db.execute(query).fetchone()
            print("DB vrátila:", user)
            success = bool(user)
            result = "Prihlásenie úspešné." if success else "Nesprávne údaje."
        except sqlite3.Error as error:
            result = f"SQL chyba: {error}"

    return render_template(
        "index.html",
        username=username,
        query=query,
        result=result,
        success=success,
    )

# @app.route("/", methods=["GET", "POST"])
# def login():
#     username = ""
#     password = ""
#     query = "SELECT * FROM users WHERE username = ? AND password = ?"
#     result = ""
#     success = False
#
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]
#         print(
#             "SQL príkaz:",
#             query,
#             f"| parametre: username={username!r}, password={password!r}",
#         )
#
#         try:
#             with sqlite3.connect(DATABASE) as db:
#                 user = db.execute(query, (username, password)).fetchone()
#             print("DB vrátila:", user)
#             success = bool(user)
#             result = "Prihlásenie úspešné." if success else "Nesprávne údaje."
#         except sqlite3.Error as error:
#             result = f"SQL chyba: {error}"
#
#     return render_template(
#         "index.html",
#         username=username,
#         query=query,
#         result=result,
#         success=success,
#     )


if __name__ == "__main__":
    setup_database()
    app.run(debug=True)
