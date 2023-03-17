from flask import Flask, render_template, redirect, request, url_for


app = Flask(__name__)

app.config["DEBUG"] = True

@app.route("/login/", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("index.html", error=False)

    #if request.form["emailInput"] != "admin" or request.form["passwordInput"] != "secret":
    if request.form['email'] != "matheus@gmail.com" and request.form['password'] != "senha":
        return render_template("index.html", error=True)
    else: 
        return redirect(url_for('main'))

    #return redirect(url_for('login'))

@app.route("/main", methods=["GET", "POST"])
def main():
    if request.method == "GET":
        print(request.json)

    return render_template("mainpage.html")

@app.route("/disciplinas", methods=["GET", "POST"])
def disciplinas():
    return render_template("disciplinaspage.html")

@app.route("/notas", methods=["GET", "POST"])
def notas():
    return render_template("notaspage.html")

@app.route("/perfil", methods=["GET", "POST"])
def perfil():
    return render_template("notaspage.html")

app.run()