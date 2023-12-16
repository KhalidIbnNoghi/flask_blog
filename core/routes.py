from flask import render_template, redirect, url_for, request, flash
from flask_login import (
    login_user,
    logout_user,
    current_user,
    login_required,
    login_user,
)

from werkzeug.security import generate_password_hash, check_password_hash

from core import app, db
from core.forms import RegistrationForm, PostForm, login_form
from core.models import User, Post, PostLike, Comment

# Основной роут отвечающий за главную страницу
@app.route("/")
@login_required
def index():
    posts = Post.query.all()
    return render_template("index.html", posts=posts, user=current_user)

# Авторизация пользователя
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = login_form()
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()
    if request.method == 'POST': 
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("index"))
        flash('Неправильный логин или пароль!')
    return render_template('login.html', form=form)

# Выход пользователя из аккаунта
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

# Регистрация пользователя
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm(request.form)
    email = request.form.get('email')
    password = request.form.get('password')
    if request.method == 'POST' and form.validate():
        user = User(email=email, password=generate_password_hash(password, method='sha256'))
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("index"))
    return render_template('register.html', form=form)

# Добавление постов
@app.route("/add_post", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if request.method == "POST":
        post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("post.html", form=form, user=current_user)

# Удаление постов
@app.route('/blog_single/delete/<int:id>',methods=['GET','POST'])
def delete(id):
    p = Post.query.filter_by(id=id).first()
    id = current_user.id
    if id == p.user_id:
        if request.method == 'GET':
            db.session.delete(p)
            db.session.commit()
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

# Редактирование постов
@app.route('/blog_single/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = db.session.query(Post).filter(Post.id==id).first()
    id = current_user.id
    if id == post.user_id:
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']

            post.title = title
            post.content = content

            db.session.commit()

            return redirect(url_for('index', id=id))

        return render_template('edit.html', post=post)
    else:
        return redirect(url_for('index'))


# Интерфейс поста с возможностью добавления комментариев
@app.route("/blog_single/<int:post_id>", methods=["GET", "POST"])
def blog_single(post_id):
    post = Post.query.get(post_id)
    id = current_user.id
    if id == post.user_id:
        comments = post.comments
        if request.method == "POST":
            comment = Comment(name=request.form.get("name"), post=post, user_id=current_user.id)
            db.session.add(comment)
            db.session.commit()
        return render_template("blog_single_user.html", post=post, comments=comments)
    else:
        comments = post.comments
        if request.method == "POST":
            comment = Comment(name=request.form.get("name"), post=post, user_id=current_user.id)
            db.session.add(comment)
            db.session.commit()
        return render_template("blog_single.html", post=post, comments=comments)

# Функционал для лайков и дизлайков постов
@app.route('/like/<int:post_id>/<action>')
@login_required
def like_action(post_id, action):
    if current_user.is_authenticated:
        post = Post.query.filter_by(id=post_id).first_or_404()
        if action == 'like':
            current_user.like_post(post)
            db.session.commit()
        if action == 'unlike':
            current_user.unlike_post(post)
            db.session.commit()
        return redirect(request.referrer)

# Страница "О сайте" с подробностями о сайте
@app.route("/about", methods=["GET", "POST"])
def about():
    return render_template("about.html")

# Страница с контактной информацией
@app.route("/contact", methods=["GET", "POST"])
def contact():
    return render_template("contact.html")
