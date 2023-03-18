from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, login_user, LoginManager, logout_user, UserMixin, current_user
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config["DEBUG"] = True

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///studentdb.db'

with app.app_context():
    db = SQLAlchemy(app)

app.secret_key = "segredobolado123456789"
login_manager = LoginManager()
login_manager.init_app(app)

class Aluno(db.Model, UserMixin):
    __tablename__ = "Aluno"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255))
    email = db.Column(db.String(255))
    senha = db.Column(db.String(255))

    def check_senha(self, senha):
        return check_password_hash(self.senha, senha)

    def get_id(self):
        return self.email


@login_manager.user_loader
def load_user(user_email):
    return Aluno.query.filter_by(email=user_email).first()

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main'))

@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("index.html", error=False)

    user = load_user(request.form['email'])

    if user == None:
        return render_template("index.html", error=True)
    
    print(user.check_senha('aa'))
    if not user.check_senha(request.form['password']):
        return render_template("index.html", error=True)

    login_user(user)
    return redirect(url_for('main'))

@app.route("/main", methods=["GET", "POST"])
def main():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    return render_template("mainpage.html")

@app.route("/disciplinas", methods=["GET", "POST"])
def disciplinas():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    return render_template("disciplinaspage.html")

@app.route("/notas", methods=["GET", "POST"])
def notas():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    return render_template("notaspage.html")

@app.route("/perfil", methods=["GET", "POST"])
def perfil():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    nome = current_user.nome
    email = current_user.email
    return render_template("perfilpage.html", nome=nome, email=email)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        #db.session.add(Aluno(id=3, nome="Luis", email="luis@gmail", senha=generate_password_hash("luissenha")))
        #db.session.commit()

    app.run()