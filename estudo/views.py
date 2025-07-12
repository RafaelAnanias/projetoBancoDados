from estudo import app, db
from flask import render_template, url_for, request, redirect, flash
from flask_login import login_user, logout_user, current_user, login_required
# Adicionar Categoria, Status e os novos formulários
from estudo.models import Lista, Categoria, Status
from estudo.forms import ListaForm, UserForm, LoginForm, CategoriaForm
# Para executar SQL puro (nossa Function)
from sqlalchemy import text

# --- A homepage, cadastro e logout permanecem iguais ---
@app.route('/', methods=['GET', 'POST'])
def homepage():
    if current_user.is_authenticated:
        return redirect(url_for('listaTarefa'))
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = form.login()
            login_user(user, remember=True)
            return redirect(url_for('listaTarefa'))
        except Exception as e:
            flash(str(e))
    return render_template('index.html', form=form)

@app.route('/cadastro/', methods=['GET', 'POST'])
def cadastro():
    form = UserForm()
    if form.validate_on_submit():
        user = form.save()
        login_user(user, remember=True)
        return redirect(url_for('listaTarefa'))
    return render_template('cadastro.html', form=form)

@app.route('/sair/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))

# --- ATUALIZAR rota novapag (adicionar tarefa) ---
@app.route('/lista/', methods=['GET', 'POST'])
@login_required
def novapag():
    form = ListaForm()
    if form.validate_on_submit():
        categoria_selecionada = form.categoria.data
        nova_lista = Lista(
            title=form.title.data,
            usuario=current_user,
            # Salvar o ID da categoria, se uma foi selecionada
            categoria_id=categoria_selecionada.id if categoria_selecionada else None
        )
        db.session.add(nova_lista)
        db.session.commit()
        flash('Tarefa adicionada com sucesso!', 'success')
        return redirect(url_for('listaTarefa'))
    return render_template('lista.html', form=form)

# --- ATUALIZAR rota listaTarefa ---
@app.route('/lista/tarefa')
@login_required
def listaTarefa():
    # TESTANDO A FUNCTION: Executando SQL puro para chamar a função
    query = text("SELECT func_contar_tarefas_concluidas(:user_id)")
    result = db.session.execute(query, {"user_id": current_user.id})
    tarefas_concluidas = result.scalar()

    # Filtra as tarefas apenas para o usuário logado
    dados = Lista.query.filter_by(user_id=current_user.id).order_by(Lista.creation_date.desc()).all()
    
    # Passa o total de tarefas concluídas para o template
    context = {'dados': dados, 'tarefas_concluidas': tarefas_concluidas}
    return render_template('lista_tarefa.html', context=context)

# --- NOVA ROTA: Para gerenciar categorias ---
@app.route('/categorias/', methods=['GET', 'POST'])
@login_required
def categorias():
    form = CategoriaForm()
    if form.validate_on_submit():
        nova_categoria = Categoria(
            nome_categoria=form.nome_categoria.data,
            usuario=current_user
        )
        db.session.add(nova_categoria)
        db.session.commit()
        flash('Categoria adicionada com sucesso!', 'success')
        return redirect(url_for('categorias'))
    
    # Busca as categorias do usuário logado para listar na página
    user_categorias = Categoria.query.filter_by(user_id=current_user.id).all()
    return render_template('categorias.html', form=form, categorias=user_categorias)

# --- NOVA ROTA: Para atualizar o status (acionará o TRIGGER) ---
@app.route('/lista/atualizar_status/<int:tarefa_id>')
@login_required
def atualizar_status(tarefa_id):
    # Encontra a tarefa e garante que pertence ao usuário logado (segurança)
    tarefa = Lista.query.filter_by(id=tarefa_id, user_id=current_user.id).first_or_404()
    
    # Assume que o Status 'Concluído' tem o ID 2
    tarefa.status_id = 2 
    db.session.commit()
    flash('Tarefa marcada como concluída!', 'success')
    return redirect(url_for('listaTarefa'))