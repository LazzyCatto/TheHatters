from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import os
from .. import db, login_manager
from ..models import User, Game
from ..forms import RegistrationForm, LoginForm

bp = Blueprint('user', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    print(form.submit)
    print(form.validate_on_submit())
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        print(username)
        print(email)
        print(password)

        if User.query.filter_by(email=email).first():
            flash('Такая почта уже существует')
            return redirect(url_for('user.register'))

        user = User(
            name=username,
            email=email
            )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()
        login_user(user)

        return redirect(url_for('games.home'))

    return render_template(
        'forms/register.html',
        form=form
        )

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('games.home'))
        else:
            flash('Неверное имя пользователя или пароль')
            return redirect(url_for('user.login'))

    return render_template(
        'forms/login.html',
        form=form
        )

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.login'))

@bp.route('/profile')
@login_required
def profile():
    created_games = current_user.created_games
    participated_games = current_user.joined_games
    pending_games = current_user.pending_games

    participated_games = [game for game in participated_games if game not in created_games]

    return render_template('profile.html',
                           user=current_user,
                           created_games=created_games,
                           participated_games=participated_games,
                           pending_games=pending_games
                           )

@bp.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    print("YA")
    if request.method == 'POST':
        # Получаем данные из формы
        name = request.form.get('name')
        about = request.form.get('about')

        # Обновляем профиль пользователя
        user = User.query.get(current_user.id)  # Предположим, что используем Flask-Login для текущего пользователя

        if user:
            user.name = name
            user.about = about
            db.session.commit()

            # Возвращаем успешный ответ
            return jsonify({
                'success': True,
                'updated_name': user.name,
                'updated_about': user.about
            })
        else:
            return jsonify({'success': False}), 400

@bp.route('/update_avatar', methods=['POST'])
@login_required
def update_avatar():
    file = request.files.get('avatar')
    if not file:
        return jsonify({'error': 'No file uploaded'}), 400

    filename = secure_filename(f'{current_user.id}_{file.filename}')
    avatar_path = os.path.join('app/static', 'avatars', filename)
    file.save(avatar_path)

    # Обновляем путь в модели пользователя
    current_user.avatar = filename
    db.session.commit()

    return jsonify({'message': 'Avatar updated successfully'})

