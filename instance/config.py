import os

SECRET_KEY_PATH = '/etc/secrets/secret_key'

def get_secret_key():
    with open(SECRET_KEY_PATH) as key_file:
        return key_file.read()

class Config:
    SECRET_KEY = get_secret_key() or 'default_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join('static', 'avatars')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    WTF_CSRF_ENABLED = False
