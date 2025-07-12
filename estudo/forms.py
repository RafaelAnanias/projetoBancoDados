from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from flask_login import current_user
from estudo import db, bcrypt
from estudo.models import Lista, User, Categoria # Adicionar Categoria
# IMPORTANTE: Adicionar o campo QuerySelectField
from wtforms_sqlalchemy.fields import QuerySelectField

# Função para buscar as categorias do usuário logado
def categorias_usuario():
    if current_user.is_authenticated:
        return Categoria.query.filter_by(user_id=current_user.id).all()
    return []

# --- O UserForm e o LoginForm permanecem exatamente iguais ---
class UserForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    sobrenome = StringField('Sobrenome', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    confirmacao_senha = PasswordField(
        'Confirmar senha',
        validators=[DataRequired(), EqualTo('senha')]
    )
    btnSubmit = SubmitField('Cadastrar')
    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Usuário já cadastrado com esse email!')
    def save(self):
        senha_hash = bcrypt.generate_password_hash(self.senha.data).decode('utf-8')
        user = User(
            nome=self.nome.data,
            sobrenome=self.sobrenome.data,
            email=self.email.data,
            senha=senha_hash
        )
        db.session.add(user)
        db.session.commit()
        return user

class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    btnSubmit = SubmitField('Login')
    def login(self):
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.senha, self.senha.data):
                return user
            else:
                raise Exception('Senha incorreta!')
        else:
            raise Exception('Usuário não encontrado!')

# --- ATUALIZAR ListaForm ---
class ListaForm(FlaskForm):
    title = StringField('Título da tarefa', validators=[DataRequired()])
    # Adicionar campo de seleção para categoria
    categoria = QuerySelectField(
        'Categoria',
        query_factory=categorias_usuario,
        get_label='nome_categoria',
        allow_blank=True,  # Permite que a tarefa não tenha categoria
        blank_text='-- Sem Categoria --'
    )
    btnSubmit = SubmitField('Enviar')

# --- NOVO: Formulário para Categoria ---
class CategoriaForm(FlaskForm):
    nome_categoria = StringField('Nome da Categoria', validators=[DataRequired()])
    btnSubmit = SubmitField('Salvar')