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

curso_disciplina = db.Table('curso_disciplinas', 
    db.Column('id_curso', db.Integer, db.ForeignKey('curso.id'), primary_key=True),
    db.Column('id_disciplina', db.Integer, db.ForeignKey('disciplina.id'), primary_key=True)
    )

class Curso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255))
    n_semestre = db.Column(db.Integer)
    disciplinas = db.relationship('Disciplina', secondary=curso_disciplina, backref='cursos')

    alunos = db.relationship('Aluno', backref="curso", lazy=True)

class Aluno(db.Model, UserMixin):
    id = db.Column('id', db.Integer, primary_key=True)
    nome = db.Column(db.String(255))
    sobrenome = db.Column(db.String(255))
    email = db.Column(db.String(255))
    senha = db.Column(db.String(255))
    id_curso = db.Column(db.Integer, db.ForeignKey('curso.id'))
    presencas = db.relationship('Presenca', backref="aluno", lazy=True)
    notas = db.relationship('Nota', backref="aluno", lazy=True)

    def check_senha(self, senha):
        return check_password_hash(self.senha, senha)

    def get_id(self):
        return self.email

class Disciplina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255))
    professor = db.Column(db.String(255))
    dia_aula = db.Column(db.Integer)
    semestre = db.Column(db.Integer)
    n_aulas = db.Column(db.Integer)
    presencas = db.relationship('Presenca', backref="disciplina", lazy=True)
    notas = db.relationship('Nota', backref="disciplina", lazy=True)

class Presenca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Integer)
    id_aluno = db.Column(db.Integer, db.ForeignKey('aluno.id'))
    id_disciplina = db.Column(db.Integer, db.ForeignKey('disciplina.id'))

class Nota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float)
    id_aluno = db.Column(db.Integer, db.ForeignKey('aluno.id'))
    id_disciplina = db.Column(db.Integer, db.ForeignKey('disciplina.id'))

def sort_disciplina(item):
    print(item.semestre)
    return item.semestre

@login_manager.user_loader
def load_user(user_email):
    return Aluno.query.filter_by(email=user_email).first()

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main'))

@app.route("/", methods=["GET", "POST"])
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
    
    curso = Curso.query.filter_by(id=current_user.id_curso).first()
    #disciplina = Disciplina.query.filter_by(id_curso=curso.id)
    print(curso.disciplinas)
    disciplinas = curso.disciplinas
    disciplinas.sort(key=sort_disciplina)
    final = disciplinas[-1].semestre

    semana = ["Domingo", "Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado"]

    print(disciplinas)
    return render_template("disciplinaspage.html", disciplinas=curso.disciplinas, semestre_final=final, semana=semana)

@app.route("/notas", methods=["GET", "POST"])
def notas():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    disciplinas = []
    for i in current_user.presencas:
        disciplinas += [Disciplina.query.filter_by(id=i.id_disciplina).first()]

    n_semestres = Curso.query.filter_by(id=current_user.id_curso).first().n_semestre

    if request.method == "POST":
        semestre = request.form["selector"]
        print(semestre)
        return render_template("notaspage.html", notas=current_user.notas, presencas=current_user.presencas, disciplinas=disciplinas, len=len(disciplinas), n_semestres=n_semestres, semestre=int(semestre))

    return render_template("notaspage.html", notas=current_user.notas, presencas=current_user.presencas, disciplinas=disciplinas, len=len(disciplinas), n_semestres=n_semestres, semestre=1)

@app.route("/perfil", methods=["GET", "POST"])
def perfil():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    nome = current_user.nome.capitalize()
    email = current_user.email
    snome = current_user.sobrenome.capitalize()
    curso = Curso.query.filter_by(id=current_user.id_curso).first().nome.capitalize()
    return render_template("perfilpage.html", nome=nome, email=email, snome=snome, curso=curso)


if __name__ == '__main__':
    app.run()