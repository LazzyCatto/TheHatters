from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from models import db, Game, User
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '756054dc75cace68a1ec2439df2cd1e840e005857bf0c074d51902ecc3624745'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

db.init_app(app)

# связываем приложение и экземпляр SQLAlchemy
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        print(name, email)
        
        # Проверяем, существует ли уже такой email
        existing_user = User.query.filter_by(email=email).first()
        print(existing_user)
        if existing_user:
            flash('Этот email уже используется!', 'danger')
            return redirect(url_for('register'))

        # Создаем нового пользователя
        new_user = User(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()
        
        # Логиним нового пользователя
        login_user(new_user)
        flash('Регистрация успешна!', 'success')
        return redirect('/')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        
        if user:
            login_user(user)  # Авторизуем пользователя
            return redirect('/')
        else:
            flash('Пользователь не найден!', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    created_games = current_user.created_games
    participated_games = current_user.games

    participated_games = [game for game in participated_games if game not in created_games]

    return render_template('profile.html',
                           user=current_user,
                           created_games=created_games,
                           participated_games=participated_games
                           )

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        title = request.form['title']
        start_time = request.form['start_time']
        start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M')
        end_time = request.form['end_time']
        end_time = datetime.strptime(end_time, '%Y-%m-%dT%H:%M')
        min_player_count = request.form['min_player_count']
        max_player_count = request.form['max_player_count']
        new_game = Game(
            title=title,
            start_time=start_time,
            end_time=end_time,
            min_player_count=min_player_count,
            max_player_count=max_player_count,
            player_count=1,
            organizer_id=current_user.id
            )
        db.session.add(new_game)
        db.session.commit()

        new_game.participants.append(current_user)
        db.session.commit()
        return redirect('/')
    return render_template('add.html')

@app.route('/delete/<int:game_id>', methods=['GET', 'POST'])
@login_required
def delete(game_id):
    game = Game.query.get_or_404(game_id)
    if game.organizer_id == current_user.id:
        if request.method == 'POST':
            db.session.delete(game)  # Удаляем игру
            db.session.commit()
            flash('Игра успешно удалена!', 'success')
            return redirect('/')
    else:
        flash('У вас нет прав на удаление этой игры.', 'danger')
        return redirect('/')
    return render_template('delete.html', game=game)

@app.route('/join_game/<int:game_id>', methods=['POST'])
@login_required
def join_game(game_id):
    game = Game.query.get_or_404(game_id)
    
    # Проверяем, что игра не полная
    if game.player_count < game.max_player_count:
        game.participants.append(current_user)  # Добавляем пользователя как участника
        game.player_count += 1  # Увеличиваем количество игроков
        
        db.session.commit()
        flash(f"Вы успешно записались на игру {game.title}", "success")
    else:
        flash(f"Игра {game.title} уже набрала максимальное количество игроков", "danger")
    
    return redirect('/')

@app.route('/leave_game/<int:game_id>', methods=['GET', 'POST'])
@login_required
def leave_game(game_id):
    game = Game.query.get_or_404(game_id)
    if current_user in game.participants:
        if request.method == 'POST':
            game.participants.remove(current_user)  # Убираем пользователя из списка участников
            game.player_count -= 1  # Уменьшаем количество игроков

            db.session.commit()
            flash(f"Вы покинули игру {game.title}.", 'info')
            return redirect('/')
    else:
        flash(f"Вы не участвуете в игре {game.title}.", 'warning')
        return redirect('/')
    return render_template('leave.html', game=game)

@app.route('/', methods=['GET'])
def songs():
    games_list = Game.query.all()
    return render_template('index.html',
                           games=games_list,
                           user=current_user if current_user.is_authenticated else None
                           )

if __name__ == '__main__':
    app.run(debug=True)