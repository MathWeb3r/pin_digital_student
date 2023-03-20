from flask_app import app, db, Aluno, Disciplina, Nota, Presenca, Curso, curso_disciplina
from werkzeug.security import generate_password_hash
from random import randrange, randint

#aluno = [id, nome, sonbrenome, email, senha, curso]
alunos = [
        [1, "luis", "pereira de souza","luis@gmail.com", "luissenha", 1],
        [2, "maria", "machado gomes", "maria@gmail.com", "mariassenha", 3],
        [3, "matheus", "gonçalves da silva", "matheus@gmail.com", "matheussenha", 2]
]

#curso = [id, nome, n_semestres]
cursos = [
        [1, "Análise de Sistemas", 5],
        [2, "Ciencia da Computação", 6],
        [3, "Engenharia de Automação", 6],
]

# disciplinas = [id, nome, professor, dia da aula, semestre, nº de aulas, id_curso]
disciplinas = [
        [1, "Introdução a programação", "Peterson", 2, 1, 20],
        [2, "Calculo I", "Jeferson", 3, 1, 25],
        [3, "Desenvolvimento Web", "William", 4, 1, 20],
        [4, "Calculo II", "Jeferson", 5, 2, 30],
        [5, "Redes de Computador", "Peterson", 6, 1, 25],
        [6, "Desafios da Engenharia", "Claudia", 6, 1, 20],
        [7, "Programação Orientada a Objetos", "William", 3, 2, 20],
        [8, "Estrutura de dados", "Júlia", 3, 3, 20],
        [9, "Sistemas Operacionas", "Rogério", 5, 2, 20],
        [10, "Sistemas Operacionas II", "Júlia", 4, 2, 20],
        [11, "Redes de Computador II", "Vitor", 5, 2, 20],
        [12, "Matemática Aplicada", "Claudia", 3, 1, 25]
]

curso_dis = [
        [1, 1], [1, 3], [1, 5], [1, 7], [1, 8], [1, 9], [1, 11],
        [2, 1], [2, 3], [2, 5], [2, 7], [2, 8], [2, 9], [2, 10], [2, 12],
        [3, 2], [3, 4], [3, 1], [3, 6], [3, 7], [3, 9]]

# notas = [id, valor, id_aluno, id_disciplina]
notas = []
id = 0
for i in range(len(alunos)):
        for n in curso_dis:
                if alunos[i][-1] == n[0]:
                        id += 1
                        notas += [[id, randrange(50, 100, 5)/10, i+1, n[1]]]

# presença = [id, valor, id_aluno, id_disciplina]
presencas = []
id = 0
for i in range(len(alunos)):
        for n in curso_dis:
                if alunos[i][-1] == n[0]:
                        id += 1
                        n_aulas = disciplinas[n[1]-1][-1]
                        presencas += [[id, randint(int(n_aulas*0.6), n_aulas), i+1, n[1]]]

print(notas)
print(presencas)

with app.app_context():
        db.drop_all()
        db.create_all()
        
        c = []
        d = []

        for i in cursos:
                c.append(Curso(id=i[0], nome=i[1], n_semestre=i[2])) 

        for i in disciplinas:
                d.append(Disciplina(id=i[0], nome=i[1], professor=i[2], dia_aula=i[3], semestre=i[4], n_aulas=i[5]))

        for curso_id in range(len(c)):
                for rel in curso_dis:
                        if rel[0]-1 == curso_id:
                                print(curso_id, c[curso_id].nome, rel[1]-1, d[rel[1]-1].nome)
                                c[curso_id].disciplinas.append(d[rel[1]-1])

        db.session.add_all(c)
        db.session.add_all(d)
        db.session.commit()

        for i in alunos:
                db.session.add(Aluno(id=i[0], nome=i[1], sobrenome=i[2], email=i[3], senha=generate_password_hash(i[4]), id_curso=i[5]))
                db.session.commit()
        

        for i in notas:
                db.session.add(Nota(id=i[0], valor=i[1], id_aluno=i[2], id_disciplina=i[3]))
                db.session.commit()
        
        for i in presencas:
                db.session.add(Presenca(id=i[0], valor=i[1], id_aluno=i[2], id_disciplina=i[3]))
                db.session.commit()

        #cursos = Curso.query.all()
        #print(cursos)
        
        '''for cu in cursos:
                print('TITLE: ', cu.nome)
                for i in cu.disciplinas:
                        print(i.nome)
                print('---')'''