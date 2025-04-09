from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from .. import db, login_manager
from ..models import User, Game, participants, pending_participants
from ..forms import RegistrationForm, LoginForm

bp = Blueprint('games', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        dates = request.form['datetimes']
        start_time, end_time = dates.split(' - ')
        start_time = datetime.strptime(start_time, '%Y/%m/%d %H:%M')
        end_time = datetime.strptime(end_time, '%Y/%m/%d %H:%M')
        min_player_count = request.form['min_players']
        max_player_count = request.form['max_players']
        validation = 'validation' in request.form

        if (not title or
            not dates or
            not start_time or
            not end_time or
            not min_player_count or
            not max_player_count):
                assert("incorrrect form")
                return redirect(url_for('user.profile'))
        
        new_game = Game(
            title = title,
            about = description,
            min_player_count = min_player_count,
            max_player_count = max_player_count,
            player_count = 1,
            start_time = start_time,
            end_time = end_time,
            validation = validation,
            organizer_id = current_user.id
        )
        db.session.add(new_game)
        db.session.commit()

        new_game.participants.append(current_user)
        db.session.commit()
        return redirect(url_for('user.profile'))
    return render_template('forms/add.html')

@bp.route('/delete/<int:game_id>', methods=['GET', 'POST'])
@login_required
def delete(game_id):
    game = Game.query.get_or_404(game_id)
    if game.organizer_id == current_user.id:
        if request.method == 'POST':
            db.session.query(participants).filter(participants.c.game_id == game.id).delete()
            db.session.query(pending_participants).filter(pending_participants.c.game_id == game.id).delete()

            db.session.delete(game)  # Удаляем игру
            db.session.commit()
            flash('Игра успешно удалена!', 'success')
            return jsonify({'status': 'redirect', 'url': url_for('user.profile')})
    else:
        flash('У вас нет прав на удаление этой игры.', 'danger')
        return jsonify({'status': 'fail'})
    return jsonify({'status': 'fail'})

@bp.route('/join/<int:game_id>', methods=['POST'])
@login_required
def join(game_id):
    game = Game.query.get_or_404(game_id)
    
    # Проверяем, что игра не полная
    if game.player_count < game.max_player_count:
        # Если игра с проверкой
        print(game.validation)
        if game.validation:
            game.pending_participants.append(current_user)
        else:
            game.participants.append(current_user)  # Добавляем пользователя как участника
            game.player_count += 1  # Увеличиваем количество игроков
        
        db.session.commit()
        flash(f"Вы успешно записались на игру {game.title}", "success")
    else:
        flash(f"Игра {game.title} уже набрала максимальное количество игроков", "danger")
        return jsonify({'status': 'fail'})
    
    return jsonify({'status': 'redirect', 'url': url_for('user.profile')})

@bp.route('/leave/<int:game_id>', methods=['GET', 'POST'])
@login_required
def leave(game_id):
    game = Game.query.get_or_404(game_id)
    if current_user in game.participants:
        if request.method == 'POST':
            game.participants.remove(current_user)  # Убираем пользователя из списка участников
            game.player_count -= 1  # Уменьшаем количество игроков

            db.session.commit()
            flash(f"Вы покинули игру {game.title}.", 'info')
            return jsonify({'status': 'redirect', 'url': url_for('user.profile')})
    elif current_user in game.pending_participants:
        if request.method == 'POST':
            game.pending_participants.remove(current_user)  # Убираем пользователя из списка участников

            db.session.commit()
            flash(f"Вы покинули игру {game.title}.", 'info')
            return jsonify({'status': 'redirect', 'url': url_for('user.profile')})
    else:
        flash(f"Вы не участвуете в игре {game.title}.", 'warning')
        return jsonify({'status': 'fail'})
    return jsonify({'status': 'fail'})

@bp.route('/', methods=['GET'])
def home():
    games = Game.query.all()  # Получаем все игры из базы данных
    events = []

    for game in games:
        extended_props = {
            'organizerName': game.organizer.name,
            'description' : game.about,
            'playerCount': game.player_count,
            'registered': current_user.is_authenticated
        }
        if current_user.is_authenticated:
            extended_props.update({
                'userCanJoin': game.player_count < game.max_player_count,
                'joined': current_user in game.participants,
                'isAuthor': game.organizer == current_user
            })

        event = {
            'title': game.title,
            'id': game.id,
            'start': game.start_time.isoformat(),
            'end': game.end_time.isoformat(),
            'extendedProps': extended_props
        }
        events.append(event)

    return render_template('index.html', events=events)
