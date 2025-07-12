from estudo import db, login_manager
from datetime import datetime
from flask_login import UserMixin

# ... (código load_user e classe User permanecem iguais) ...
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    sobrenome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    # Relacionamentos
    listas = db.relationship('Lista', backref='usuario', lazy=True)
    categorias = db.relationship('Categoria', backref='usuario', lazy=True)

class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_status = db.Column(db.String(50), nullable=False, unique=True)
    listas = db.relationship('Lista', backref='status', lazy=True)

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_categoria = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # IMPORTANTE: Adicione esta linha para exibir o nome no formulário
    def __repr__(self):
        return self.nome_categoria

class Lista(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.DateTime, default=datetime.now)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False, default=1)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=True)
  
class LogAtualizacaoTarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tarefa_id = db.Column(db.Integer, db.ForeignKey('lista.id', ondelete='CASCADE'), nullable=False)
    status_anterior_id = db.Column(db.Integer)
    status_novo_id = db.Column(db.Integer)
    data_hora = db.Column(db.DateTime, default=datetime.now)
