from flask import Flask, render_template, request


app = Flask(__name__)

app.config["DEBUG"] = True

@app.route("/login/", methods=["GET", "POST"])
def hello_world():

    if request.method == "GET":
        return render_template("index.html", error=False)

    #if request.form["emailInput"] != "admin" or request.form["passwordInput"] != "secret":
    if request.method == "POST":
        print(request.form["emailInput"], request.form["passwordInput"])

    return render_template("index.html")

app.run()